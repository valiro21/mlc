# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import tornado.web
from sqlalchemy.exc import SQLAlchemyError

from BackendServer.handlers.BaseHandler import BaseHandler
from DB.Entities import Job, Testcase
from DB.Repositories import SubmissionRepository, ProblemRepository


class PrettyWrapper:
    def __init__(self,
                 job,
                 testcase):
        self.testcase = testcase
        self.job = job


class SubmissionDetailsHandler(BaseHandler):
    def get(self):
        """
        Handler for submission details. Binded at path /submission?id=<id>
        Throws Tornado 404 error if submission id is invalid in any way.
        """
        submission_id = self.get_argument("id", None)
        if submission_id is None:
            raise tornado.web.HTTPError(404,
                                        "A submission id must be supplied")

        try:
            submission_id = int(submission_id)
        except ValueError:
            raise tornado.web.HTTPError(404,
                                        "Submission id must be integer")

        session = self.acquire_sql_session()

        try:
            submission = SubmissionRepository.get_by_id(session, submission_id)
        except SQLAlchemyError:
            raise tornado.web.HTTPError(404,
                                        "Must be a valid submission id")

        problem = ProblemRepository.get_by_id(session, submission.problem_id)
        active_dataset_id = problem.active_dataset_id

        results = session.query(Job, Testcase) \
            .filter(Job.submission_id == submission_id) \
            .filter(Job.dataset_id == active_dataset_id) \
            .join(Testcase, Job.testcase_id == Testcase.id)\
            .all()

        if len(results) == 0:
            # Compiling or has already compiled
            results = session.query(Job) \
                .filter(Job.submission_id == submission_id)\
                .one()
            self.render("submission_details.html",
                        submission=submission,
                        testcases=PrettyWrapper(results, None))
            return

        return_list = []
        for row in results:
            job, testcase = row
            return_list.append(PrettyWrapper(job, testcase))

        self.render("submission_details.html",
                    submission=submission,
                    testcases=return_list)
