# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
import datetime
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import psycopg2
import psycopg2.extensions
import tornado.ioloop

from sqlalchemy import or_
from tornado import concurrent

from DB import session_factory
from DB.Entities.Job import Job
from Worker.Sandboxes import sandbox
from Worker.Sandboxes.JobResult import AbortJobResult
from Worker.Sandboxes.WorkerSandbox import WorkerSandbox
from DB import config

io_loop = tornado.ioloop.IOLoop.instance()

conn = psycopg2.connect(host=config['database_host'],
                        dbname=config['database_name'],
                        user=config['database_user'],
                        password=config['database_password'],
                        connect_timeout=5)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)


class InternalError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(InternalError, self).__init__(message)


class WorkerProcess:
    """
    This class is the brain of the worker. It can listen and
    talk using postgres push notification feature and also
    constantly checks for new operations.

    Workflow:

    (1) Initialize contest cache
            |                                            Evaluation loop
  |---------|-----------------------------------------------------------------|
  |         |                                                                 |
  |         V                  If jobs available                              |
  | (2) Select available jobs -------------------> (3) Evaluate the jobs      |
  |        | ^             ^                                   |              |
  |        | |             |                                   |              |
  |    No  | |   On        |                                   v              |
  |   more | | notify      |----------------------- (4) Mark jobs finished    |
  |   jobs | |                                                                |
  |        | |                                                                |
  |--------|-|----------------------------------------------------------------|
           v |
    (5) Start listen on database channel if not listening
           |
           |
           v
    (6) Send notification on database channel to make sure
        we didn't miss anything
    """

    MAX_BATCH_OPERATIONS = 3
    MAX_COMPILE_TIME = 3

    def listen(self):
        """
        Initiate listen to the registered channel.
        """
        curs = conn.cursor()
        curs.execute("LISTEN %s;" % self.channel)

    def receive(self):
        """
        Handler for chanel events.
        :param fd: File descriptors for the connection
        :param events: Events that are currently registered
        :return:
        """

        def _receive(fd, events):
            state = conn.poll()
            if state == psycopg2.extensions.POLL_OK:
                if conn.notifies:
                    notify = conn.notifies.pop()
                    if notify.payload == 'work!' and \
                            not self.in_evaluation_loop:
                        self.execute_evaluation_loop()

        return _receive

    def talk(self, what="", delay=5):
        """
        Talk to someone through a chanel.
        :param what: The very important message
        :param delay: Speak afer delay time in seconds.
        """
        # Connections are thread-safe, but cursors are not
        curs = conn.cursor()

        # Notify all of what you just said
        def _talk():
            time.sleep(delay)
            curs.execute("NOTIFY %s, '%s';" %
                         (self.channel, what))
            print("Looking for missing jobs")

        threading.Thread(target=_talk).start()

    def __init__(self, ioloop, channel):
        """
        Initialize the Worker in the main thread.
        :param ioloop: The main tornado ioloop.
        :param channel:  The channel being listened.
        """
        self.jobs = []
        self.ioloop = ioloop  # Main tornado ioloop
        self.channel = channel  # Channel to listen and send messages to
        self.results = []
        self.tasks = 0
        self.running_jobs = []
        self.jobs_futures = []
        self.executor = ThreadPoolExecutor(
            max_workers=self.MAX_BATCH_OPERATIONS)

        self.init_cache()
        self.execute_evaluation_loop()
        # Receive a kick in the nuts when somebody talks
        io_loop.add_handler(conn.fileno(), self.receive(), io_loop.READ)

        # Always listen before talking
        print("Attached database listener")
        self.listen()
        self.talk("work!")

    def init_cache(self):
        """"
        Step 1 of the workflow. Download all testcases
        where the worker was assigned.
        """
        self.sandbox = WorkerSandbox()
        self.sandbox.prepare()

    def execute_evaluation_loop(self):
        self.is_evaluation_loop = True

        self.update_jobs_list()
        while len(self.jobs) > 0 or len(self.jobs_futures) > 0:
            self.execute_jobs()
            self.mark_finished()
            self.update_jobs_list()

        self.in_evaluation_loop = False

    def update_jobs_list(self):
        """
        Step 2 of the workflow. Get a list of pending jobs.
        """

        # Very unsafe. Keep the session open and close in Step 4.
        self.session = session_factory()
        self.session.expire_on_commit = False
        self.available_tasks = self.MAX_BATCH_OPERATIONS - \
            len(self.jobs_futures)
        self.jobs = []
        if self.available_tasks <= 0:
            return

        try:
            current_time = datetime.datetime.now()
            self.jobs = self.session.query(Job) \
                .filter(Job.status == 1) \
                .filter(or_(Job.estimated_finish_timestamp == None,
                            Job.estimated_finish_timestamp < current_time)) \
                .limit(self.available_tasks) \
                .all()

            for job in self.jobs:
                next_timestamp = datetime.datetime.now()
                if job.job_type == 'Compile':
                    next_timestamp += datetime.timedelta(
                        milliseconds=int(self.MAX_COMPILE_TIME * 1000.0) +
                        2000)
                elif job.job_type == 'Evaluate':
                    next_timestamp += datetime.timedelta(
                        milliseconds=int(job.time_limit * 1000.0) + 2000)
                job.estimated_finish_timestamp = next_timestamp
                self.session.commit()
        except Exception as err:
            print(err)
            self.session.rollback()

    def execute_jobs(self):
        """"
        Step 3 of the workflow. Execute the pending jobs.
        """
        self.results = []
        worker_id = 0
        for job in self.jobs:
            key = (job.submission_id, job.dataset_id, job.testcase_id)
            # Add jobs if not already evaluation
            if key in self.running_jobs:
                continue
            self.running_jobs.append(key)

            sid = int(job.submission_id)

            if job.job_type == 'Compile':
                future = self.executor.submit(sandbox.compile,
                                              sid)
                self.jobs_futures.append(future)
            elif job.job_type == 'Evaluate':
                future = self.executor.submit(self.sandbox.evaluate,
                                              job.problem_id,
                                              job.dataset_id,
                                              job.testcase_id,
                                              job.submission_id,
                                              worker_id)
                self.jobs_futures.append(future)
            worker_id += 1

    def mark_finished(self):
        """"
        Step 4 of the workflow. Mark the finished jobs in the database
        and update the status message.
        """

        self.session.close()

        try:
            session = session_factory()
        except:
            print("Failed to open connection")
            return

        try:
            changed_jobs = []

            futures = concurrent.futures.wait(self.jobs_futures, timeout=3)
            self.jobs_futures = []
            self.jobs_futures.extend(futures[1])

            for future in futures[0]:
                if future.cancelled():
                    continue

                submission_id, dataset_id, testcase_id, job_result = \
                    future.result()

                key = (submission_id, dataset_id, testcase_id)
                self.running_jobs.remove(key)

                # Add jobs if not already evaluation
                if key in self.running_jobs:
                    continue

                if isinstance(job_result, AbortJobResult):
                    print(job_result)
                    raise InternalError(job_result.message)
                job = session.query(Job) \
                    .filter(Job.submission_id == submission_id) \
                    .filter(Job.dataset_id == dataset_id) \
                    .filter(Job.testcase_id == testcase_id) \
                    .one()
                job.status = 2
                job.status_code = job_result.code
                job.status_message = job_result.message
                job.cpu = job_result.cpu
                job.memory = job_result.memory
                changed_jobs.append(job)
            session.commit()
        except concurrent.futures.TimeoutError:
            session.commit()
        except InternalError as err:
            print(err)
            session.rollback()
        finally:
            session.close()
