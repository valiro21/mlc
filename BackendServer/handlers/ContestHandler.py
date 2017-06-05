# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

# coding=utf-8
"""Contest Handler for contest page."""

import os

from sqlalchemy.exc import SQLAlchemyError

from BackendServer.handlers.BaseHandler import BaseHandler

from DB import Participation
from DB.Repositories import ContestRepository, UserRepository
from DB.Repositories.ParticipacionRepository import ParticipationRepository


class ContestHandler(BaseHandler):
    """Tornado handler for a contest."""

    def data_received(self, chunk):
        pass

    def post(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        operation_type = path_elements[2]
        if operation_type == 'register':
            try:
                self.get_argument('agree')
            except:
                self.render('contest_fail_register.html',
                            reason='you did not accept the terms')
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
                self.render('contest_fail_register.html',
                            reason='contest is private')
                return
            elif contest.type == 2:
                self.render('contest_fail_register.html',
                            reason='contest is public but not open')
                return

            ok = ParticipationRepository. \
                verif_participation(session, user.id, contest.id)

            if ok:
                self.render('contest_fail_register.html',
                            reason='you are already ' +
                                   'registered for this contest')
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

        self.render("contest_" +
                    path_elements[2] +
                    ".html", contest_id=contest_name)
