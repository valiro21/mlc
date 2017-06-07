# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from BackendServer.handlers.BaseHandler import BaseHandler


from DB.Entities import Submission, Participation, Contest, Problem, User
from DB.Repositories import ContestRepository, SubmissionRepository, \
    UserRepository
from DB.Repositories import ProblemRepository


class PrettyWrap:
    """
    Wrap a problem, contest, submission and user
    and information about the scoring.
    """

    def __init__(self,
                 submission,
                 contest,
                 problem,
                 user,
                 message,
                 cpu,
                 memory):
        self.submission = submission
        self.contest = contest
        self.problem = problem
        self.user = user
        self.message = message
        self.cpu = cpu
        self.memory = memory


class SubmissionsHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        """
        Render page with submissions. Parameters:
         * required pg_number: The page number to show
         * user: The name of the username to show submissions of
         * problem: The name of the problem to show submission for
         * contest: The name of the contest where the contest was submitted
        """
        contest_name = self.get_argument("contest", None)  # Contest name
        problem_name = self.get_argument("problem", None)  # Problem name
        user_name = self.get_argument("user", None)  # Problem name
        pg_nr = self.get_argument("page_number", "1")  # Page number
        pg_size = 20  # Defaults to 20 submissions per page

        try:  # Try to fetch page number. Should be integer.
            pg_nr = int(pg_nr)
        except ValueError:
            self.render("submissions.html",
                        submissions=None,
                        error="Invalid page number, "
                              "should be a valid integer")

        try:
            session = self.acquire_sql_session()
        except SQLAlchemyError as err:
            print(str(SQLAlchemyError))
            self.render("submissions.html",
                        submissions=None,
                        error="Database is down!")
            return

        try:
            # Get problem or None if not required
            if problem_name is not None:
                problem = ProblemRepository.get_by_name(session, problem_name)
                problem_id = problem.id
            else:
                problem_id = None

            # Get contest or None if not required
            if contest_name is not None:
                contest = ContestRepository.get_by_name(session, contest_name)
                contest_id = contest.id
            else:
                contest_id = None

            # Get user or None if not required
            if user_name is not None:
                user = UserRepository.get_by_name(session, user_name)
                user_id = user.id
            else:
                user_id = None
        except MultipleResultsFound:
            session.close()
            self.render("submissions.html",
                        submissions=None,
                        error="Invalid database!")
            return
        except NoResultFound:
            session.close()
            self.render("submissions.html",
                        submissions=None,
                        error="Invalid contest or problem parameters")
            return

        # Done handling errors

        # Create multiple part query
        query = session.query(Submission, Contest, Problem, User) \
            .join(Participation,
                  Submission.participation_id == Participation.id)\
            .join(User, User.id == Participation.user_id)\
            .join(Contest, Contest.id == Participation.contest_id)\
            .join(Problem, Problem.id == Submission.problem_id)

        if user_id is not None:
            query = query.filter(User.id == user_id)

        if contest_id is not None:
            query = query.filter(Contest.id == contest_id)

        if problem_id is not None:
            query = query.filter(Problem.id == problem_id)

        query.order_by(desc(Submission.created_timestamp))\
            .limit(pg_nr * pg_size)\
            .offset((pg_nr - 1) * pg_size)\
            .limit(pg_size)

        results = query.all()
        return_list = []
        for row in results:
            submission, contest, problem, user = row
            score = SubmissionRepository.get_status(session, submission.id)

            wrapper = PrettyWrap(submission,
                                 contest,
                                 problem,
                                 user,
                                 score[0],  # Message to show
                                 score[1],  # Cpu used
                                 score[2])  # Memory used
            return_list.append(wrapper)

        session.close()

        self.render("submissions.html", submissions=return_list)
