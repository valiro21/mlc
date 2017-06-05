# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from DB.Entities import Base


class Job(Base):
    """
    Class used to describe a job for a worker.
    For example we need to evaluate testcase 4 on problem 2
    in contest 1. This table is used for queueing tasks.
    """
    __tablename__ = 'jobs'

    submission_id = Column(Integer, nullable=False, primary_key=True)
    submission_id.__doc__ = 'ID of the submission'

    problem_id = Column(Integer, primary_key=True)
    problem_id.__doc__ = 'ID of the submission'

    dataset_id = Column(Integer, default=-1, primary_key=True)
    dataset_id.__doc__ = 'ID of the dataset'

    testcase_id = Column(Integer, default=-1, primary_key=True)
    testcase_id.__doc__ = 'ID of the testcase'

    job_type = Column(String)
    job_type.__doc__ = 'The type of the task.'

    status_code = Column(Integer, nullable=True)
    status_code.__doc__ = 'Compilation or evaluation return code.'

    status_message = Column(String, nullable=True)
    status_message.__doc__ = 'Compilation or evaluation message.'

    time_limit = Column(Float, nullable=False, default=1)
    time_limit.__doc__ = 'Time limit in seconds.'

    memory_limit = Column(Float, nullable=False, default=64)
    memory_limit.__doc__ = 'Memory limit in MB'

    created_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    created_timestamp.__doc__ = 'The timestamp when the task was created.'

    estimated_finish_timestamp = Column(DateTime, nullable=True, default=None)
    estimated_finish_timestamp.__doc__ = 'The expected timestamp when ' \
                                         'the job should be finished.'

    worker_id = Column(Integer, nullable=True)
    worker_id.__doc__ = 'The id of the worker that executes the job.'

    status = Column(Integer, nullable=False, default=1)
    status.__doc__ = 'Status of the job.'

    score = Column(Integer, nullable=True)
    score.__doc__ = 'Score given by a scoring heuristic to determine ' \
                    'the execution priority.'

    cpu = Column(Float, nullable=True, default=None)
    cpu.__doc__ = 'Cpu used.'

    memory = Column(Float, nullable=True, default=None)
    memory.__doc__ = 'Memory used.'
