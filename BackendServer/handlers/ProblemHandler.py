# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import os

from sqlalchemy.orm.exc import NoResultFound
from tornado.web import HTTPError

from BackendServer.handlers.BaseHandler import BaseHandler
from DB.Entities import Submission, Participation
from DB.Repositories import ProblemRepository, \
    ContestRepository, \
    UserRepository


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

        print('Receiving submission...')

        submission_code = self.get_body_argument("data", None)
        contest_id = int(self.get_argument("contest_id", 1))  # 1 is archive
        language = self.get_argument("lang")
        problem_name = self.get_problem_by_path()

        if problem_name is None:
            print("Problem is None")
            return

        session = self.acquire_sql_session()
        try:
            problem = ProblemRepository.get_by_name(session, problem_name)
            # contest = ContestRepository.get_by_id(session, contest_id)

            # TODO: check if user can submit to the problem
            # case: Contest is private (check Participation first)
            # case: Problem does not belong to archive

            if problem.datasets is None or len(problem.datasets) == 0:
                self.write("FAILED")
                print('No datasets')
                return

            if self.get_current_user() is None:
                self.write("must be logged in")
                print('Not logged in')
                return

            username = self.get_current_user()
            user = UserRepository.get_by_name(session, username)

            participation = session\
                .query(Participation)\
                .filter(Participation.user_id == user.id)\
                .filter(Participation.contest_id == contest_id)\
                .limit(1)\
                .one()

            # for dataset in problem.datasets:
            submission = Submission(problem_id=problem.id,
                                    participation_id=participation.id,
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

        print('Addded submission.')
        self.write("OK")

    def get(self):
        """
        Tornado Request handler for a problem.
        The first path of the url is '/problem'
        The problem name must be the second path of the url.
        The page for a required problem is the third part of the url:
        '/statement' - See the statement and editor.
        '/comments' - Comments section.
        '/submissions' - Submissions for this problem.
        '/editorial' - Editorial for this problem.
        '/pdf?id=<number>' - The statement number to fetch

        '?contest_id=<number> - Tests if problem belongs to contest,
                                and changes page to reflect it

        """
        path_elements = [x for x in self.request.path.split("/") if x]
        problem_name = path_elements[1]

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Failed to acquire database session.')

        try:
            problem = ProblemRepository.get_by_name(session, problem_name)
        except NoResultFound:
            raise HTTPError(404, 'Problem not found')

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

        contest_id = self.get_argument('contest_id', None)

        try:
            contest = ContestRepository.get_by_id(session, contest_id)
            problem = ProblemRepository.get_by_name(session, problem_name)

            if not ContestRepository.has_problem(session,
                                                 contest_id=contest_id,
                                                 problem_id=problem.id):
                contest = None
        except:
            contest = None

        if path_elements[2] == 'submissions':
            self.redirect('/submissions?problem=' + problem_name)

        self.render("problem_" +
                    path_elements[2] +
                    ".html", problem=problem,
                    pdf_id=pdf_id,
                    contest=contest)
        session.close()
