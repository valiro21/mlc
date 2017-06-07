# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

# coding=utf-8
"""Contest Handler for contest page."""

import os

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from BackendServer.handlers.BaseHandler import BaseHandler
from BackendServer.handlers.SubmissionsHandler import PrettyWrap

from DB import Participation
from DB.Entities import Submission, Contest, Problem, User
from DB.Repositories import ContestRepository, \
    UserRepository, \
    SubmissionRepository
from DB.Repositories.ParticipacionRepository import ParticipationRepository


class ContestHandler(BaseHandler):
    """Tornado handler for a user contest."""

    def data_received(self, chunk):
        pass

    def post(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        operation_type = path_elements[2]
        if operation_type == 'register':
            try:
                self.get_argument('agree')
            except:
                self.write('You did not accept the terms!')
                return

            participation_type = self.get_argument('participation_type')
            contest_name = path_elements[1].replace('%20', ' ')
            user_name = self.get_current_user()
            session = self.acquire_sql_session()

            try:
                contest = ContestRepository.get_by_name(session, contest_name)
                user = UserRepository.get_by_name(session, user_name)
            except SQLAlchemyError as e:
                self.redirect("register")
                print(e)
                return

            if contest.type == 3:
                self.write('Contest is private')
                return
            elif contest.type == 2:
                self.write('Contest is public but not open')
                return

            ok = ParticipationRepository. \
                verif_participation(session, user.id, contest.id)

            if ok:
                self.write('You are already registered for this contest')
                return

            participation = Participation(user_id=user.id,
                                          contest_id=contest.id,
                                          type=participation_type)

            try:
                session.add(participation)
                session.commit()
            except SQLAlchemyError as e:
                self.redirect("register")
                print(e)
                return
        self.redirect("contest_done_register")

    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        contest_name = path_elements[1].replace('%20', ' ')

        session = self.acquire_sql_session()
        contest = ContestRepository.get_by_name(session, contest_name)
        user_name = self.get_current_user()
        user = UserRepository.get_by_name(session, user_name)

        problems = ContestRepository.get_all_problems(session, contest.id)

        for problem in problems:
            print(problem)

        if contest.type == 3:
            ok = ParticipationRepository. \
                verif_participation(session, user.id, contest.id)

            if ok is False:
                self.redirect('..')
                return

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "problems"))
            return

        if path_elements[2] == 'register':
            self.render("contest_register.html",
                        contest_id=contest_name)
            return

        if len(path_elements) >= 4:
            self.redirect("..")
            return

        if path_elements[2] == 'submit' or \
                path_elements[2] == 'mysubmissions':
            ok = ParticipationRepository. \
                verif_participation(session, user.id, contest.id)

            if ok is False:
                self.render('contest_fail_non_registered.html')
                return

        if path_elements[2] not in ["problems",
                                    "submit",
                                    "mysubmissions",
                                    "submissions",
                                    "standings"]:
            self.redirect("problems")

        if path_elements[2] in ['submissions', 'mysubmissions']:
            query = session.query(Submission, Contest, Problem, User) \
                .join(Participation,
                      Submission.participation_id == Participation.id) \
                .join(User, User.id == Participation.user_id) \
                .join(Contest, Contest.id == Participation.contest_id) \
                .join(Problem, Problem.id == Submission.problem_id)

            if path_elements[2] == 'mysubmissions':
                query = query.filter(User.id == user.id)

            if contest.id is not None:
                query = query.filter(Contest.id == contest.id)

            query.order_by(desc(Submission.created_timestamp))

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

            self.render("contest_submissions.html",
                        contest_id=contest.id,
                        submissions=return_list)
            return

        self.render("contest_" +
                    path_elements[2] + ".html",
                    contest_id=contest_name,
                    problems=problems)
