# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import os

from tornado.web import HTTPError

from BackendServer.handlers.BaseHandler import BaseHandler

from DB.Entities import Submission
from DB.Repositories import ProblemRepository


class ProblemHandler(BaseHandler):
    """Tornado handler for a problem."""
    def data_received(self, chunk):
        pass

    def get_problem_by_path(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        if len(path_elements) < 2:
            return None
        return path_elements[1]

    def post(self):
        submission_code = self.get_body_argument("data", None)
        language = self.get_argument("lang")
        problem_name = self.get_problem_by_path()

        if problem_name is None:
            return

        session = self.acquire_sql_session()
        try:
            problem = ProblemRepository.get_by_name(session, problem_name)

            # TODO: check if user can submit to the problem
            # case: Contest is private (check Participation first)
            # case: Problem does not belong to archive

            if problem.datasets is None or len(problem.datasets) == 0:
                self.write("FAILED")
                return

            for dataset in problem.datasets:
                submission = Submission(problem_id=problem.id,
                                        participation_id=None,
                                        file=submission_code.encode('utf8'),
                                        language=language
                                        )
                session.add(submission)
            session.commit()
        except Exception as e:  # Something went wrong
            session.rollback()
            print(e)
            self.write("FAILED")
            return
        finally:
            session.close()

        self.write("OK")

    def get(self):
        """
        Tornado Request handler for a problem.
        The first path of the url is '/problem'
        The problem name must be the second path of the url.
        The page for a required problem is the third part of the url:
        '/statement' - See the statement and editor.
        '/comments' - Comments section.
        '/submission' - Submissions for this problem.
        '/editorial' - Editorial for this problem.
        '/pdf?id=<number>' - The statement number to fetch


        """
        path_elements = [x for x in self.request.path.split("/") if x]
        problem_name = path_elements[1]

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Failed to acquire database session.')

        try:
            problem = ProblemRepository.get_by_name(session, problem_name)
        except:
            raise HTTPError(500, 'A database error has occured')

        if problem is None:
            raise HTTPError(404)

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "statement"))
            return
        if len(path_elements) >= 4:
            self.redirect("..")
            return
        pdf_id = self.get_argument("id", None)
        if pdf_id is None:
            pdf_id = 0  # Defaults to the first statement
        else:
            pdf_id = int(pdf_id)

        # Avoid out of bounds and get the first item
        if problem.statements is not None and \
           (pdf_id >= len(problem.statements) or pdf_id < 0):
            pdf_id = 0

        if path_elements[2] == 'pdf':
            if problem.statements is not None and \
                            pdf_id < len(problem.statements):
                # Set application type
                self.set_header("Content-Type",
                                'application/pdf; charset="utf-8"')

                # The actual file headers
                self.set_header("Content-Disposition",
                                "inline; filename=statement.pdf")

                # File content
                self.write(problem.statements[pdf_id])
                return
            return

        if path_elements[2] not in ["statement",
                                    "submissions",
                                    "editorial",
                                    "comments"]:
            self.redirect("statement")

        session.close()

        self.render("problem_" +
                    path_elements[2] +
                    ".html", problem=problem,
                    pdf_id=pdf_id)
