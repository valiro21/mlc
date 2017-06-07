# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

# coding=utf-8
"""UserHandler for contestants."""

import os

from sqlalchemy import desc
from tornado.web import HTTPError
from BackendServer.handlers.BaseHandler import BaseHandler
from BackendServer.handlers.SubmissionsHandler import PrettyWrap
from DB.Entities import Submission, Contest, Problem, User, Participation
from DB.Repositories import SubmissionRepository, UserRepository


class UserHandler(BaseHandler):
    """Tornado handler for a user."""

    def data_received(self, chunk):
        pass

    def get(self):

        path_elements = [x for x in self.request.path.split("/") if x]
        username = path_elements[1]

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "profile"))
            return
        if len(path_elements) >= 4:
            self.redirect("..")
            return

        if path_elements[2] not in ["profile",
                                    "settings",
                                    "user_submissions",
                                    "user_contests",
                                    "user_statistics"]:
            self.redirect("profile")

        if path_elements[2] == 'user_submissions':
            # Get all user submissions for the user

            session = self.acquire_sql_session()

            pg_nr = int(self.get_argument("page_number", "1"))  # Page number
            pg_size = 20  # Defaults to 20 submissions per page

            # Create multiple part query
            query = session.query(Submission, Contest, Problem, User) \
                .join(Participation,
                      Submission.participation_id == Participation.id) \
                .join(User, User.id == Participation.user_id) \
                .join(Contest, Contest.id == Participation.contest_id) \
                .join(Problem, Problem.id == Submission.problem_id)

            if username is not None:
                query = query.filter(User.username == username)

                user = session.query(User)\
                    .filter(User.username == username).one_or_none()
                if user is None:
                    self.render('profile_not_found.html')
                try:
                    db_user = UserRepository.get_by_name(session, username)
                except:
                    raise HTTPError(404, 'Could not find requested user.')

            query.order_by(desc(Submission.created_timestamp)) \
                .limit(pg_nr * pg_size) \
                .offset((pg_nr - 1) * pg_size) \
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

            self.render("user_submissions.html",
                        user=db_user,
                        submissions=return_list)
            return

        session = self.acquire_sql_session()
        user = session.query(User)\
            .filter(User.username == username).one_or_none()

        if user is None:
            self.render("profile_not_found.html")

        else:
            self.render(path_elements[2] + ".html",
                        user=user, user_id=user.username)
