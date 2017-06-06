"""ContestHandler for AdminServer. This is used for updating contests. """

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
import calendar
import os
import time
import traceback
from datetime import datetime

import tornado
from sqlalchemy import update
import tornado.web
from sqlalchemy.sql.elements import and_
from tornado.web import HTTPError
from sqlalchemy.exc import SQLAlchemyError

from AdminServer.handlers import BaseHandler

from DB import Contest, Participation
from DB.Repositories import ContestRepository, UserRepository
from DB.Repositories.ParticipacionRepository import ParticipationRepository


class ContestHandler(BaseHandler.BaseHandler):
    """Handler for login."""

    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def post(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        contest_id = path_elements[1]
        if len(path_elements) == 2 and contest_id == "create":
            contest_name = self.get_argument('contest_name')
            start_date_string = self.get_argument('start_date')

            start_date = \
                datetime.strptime(start_date_string, '%m/%d/%Y %I:%M %p')

            start_date_utc = calendar.timegm(start_date.timetuple())

            end_date_string = self.get_argument('end_date')
            end_date = datetime.strptime(end_date_string, '%m/%d/%Y %I:%M %p')
            end_date_utc = calendar.timegm(end_date.timetuple())

            try:
                session = self.acquire_sql_session()
            except:
                traceback.print_exc()
                # TODO: handle error
                return

            try:
                new_contest = Contest(name=contest_name,
                                      description='',
                                      start_time=start_date_utc,
                                      end_time=end_date_utc)
                session.add(new_contest)
                session.commit()
            except SQLAlchemyError as e:
                self.redirect("create")
                print(e)
                return

            self.redirect_to_settings(self, contest_name + "/settings")
            session.close()
            return

        elif len(path_elements) == 3 and path_elements[2] == 'settings':
            contest_name = self.get_argument('contest_name')
            contest_description = self.get_argument('contest_description')
            contest_type = self.get_argument('contest_type')

            contest_dict = {
                'Open': 1,
                'Public': 2,
                'Private': 3
            }

            contest_type = contest_dict.get(contest_type, 1)

            try:
                self.get_argument('contest_virtual')
                contest_virtual = True
            except:
                contest_virtual = False
            try:
                self.get_argument('contest_allow_download')
                contest_allow_download = True
            except:
                contest_allow_download = False
            try:
                self.get_argument('contest_allow_questions')
                contest_allow_questions = True
            except:
                contest_allow_questions = False
            try:
                self.get_argument('contest_allow_usertest')
                contest_allow_usertest = True
            except:
                contest_allow_usertest = False

            contest_restricted_ip = \
                self.get_argument('contest_restricted_ip')

            contest_start_time_string = \
                self.get_argument('contest_start_time')

            contest_start_time_non_utc = \
                datetime.strptime(contest_start_time_string,
                                  '%m/%d/%Y %I:%M %p')

            contest_start_time = \
                calendar.timegm(contest_start_time_non_utc.timetuple())

            contest_end_time = \
                self.get_argument('contest_end_time')

            contest_end_time_non_utc = \
                datetime.strptime(contest_end_time, '%m/%d/%Y %I:%M %p')

            contest_end_time = \
                calendar.timegm(contest_end_time_non_utc.timetuple())

            # contest_timezone = \
            # self.get_argument('contest_timezone')# make date time picker boss
            contest_max_submissions = \
                self.get_argument('contest_max_submissions')
            contest_max_user_tests = \
                self.get_argument('contest_max_user_tests')
            contest_submission_delay = \
                self.get_argument('contest_min_submission_interval')
            contest_user_test_delay = \
                self.get_argument('contest_min_user_test_interval')

            try:
                session = self.acquire_sql_session()
            except:
                traceback.print_exc()
                # TODO: handle error
                return

            try:
                contest_old_name = path_elements[1]
                stmt = update(Contest). \
                    where(Contest.name == contest_old_name). \
                    values(name=contest_name,
                           description=contest_description,
                           type=contest_type,
                           virtual=contest_virtual,
                           submission_download_allowed=contest_allow_download,
                           allow_questions=contest_allow_questions,
                           allow_user_test=contest_allow_usertest,
                           restricted_ip=contest_restricted_ip,
                           start_time=contest_start_time,
                           end_time=contest_end_time,
                           max_submissions=contest_max_submissions,
                           max_user_test=contest_max_user_tests,
                           min_submission_interval=contest_submission_delay,
                           min_user_test_interval=contest_user_test_delay,
                           )
                session.execute(stmt)
                session.commit()
            except SQLAlchemyError as e:
                print(e)
                self.redirect_to_settings(self, "settings")
                return
            self.redirect("problems")
            session.close()

        elif len(path_elements) == 3 and path_elements[2] == 'addusers':
            session = self.acquire_sql_session()
            contest_name = path_elements[1]
            user_name = self.get_argument('username')
            participation_type = self.get_argument('participation_type')
            delay_time = self.get_argument('delay_time')
            extra_time = self.get_argument('extra_time')
            s_password = self.get_argument('special_password')

            if s_password == '':
                s_password = None
            try:
                self.get_argument('unrestricted')
                unrestricted = True
            except:
                unrestricted = False

            try:
                self.get_argument('hidden')
                hidden = True
            except:
                hidden = False

            try:
                contest = ContestRepository.get_by_name(session, contest_name)
                user = UserRepository.get_by_name(session, user_name)
            except SQLAlchemyError as e:
                self.write('User or Contest not found!')
                print(e)
                return
            if contest is None:
                self.write('Contest is None!')
            if user is None:
                self.write('User is None!')

            ok = ParticipationRepository. \
                verif_participation(session, user.id, contest.id)

            if ok is False:
                participation = Participation(user_id=user.id,
                                              contest_id=contest.id,
                                              type=participation_type,
                                              unrestricted=unrestricted,
                                              hidden=hidden,
                                              delay_time=delay_time,
                                              extra_time=extra_time,
                                              special_password=s_password)
                session.add(participation)
                session.commit()
                message = 'registered'
            else:
                stmt = update(Participation). \
                    where(and_(Participation.user_id == user.id,
                          Participation.contest_id == contest.id)). \
                    values(type=participation_type,
                           unrestricted=unrestricted,
                           hidden=hidden,
                           delay_time=delay_time,
                           extra_time=extra_time,
                           special_password=s_password)
                session.execute(stmt)
                session.commit()
                message = 'registered'
            self.write(message)
            return

    @tornado.web.authenticated
    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        if len(path_elements) == 1:
            self.render("contests.html")
            return
        contest_name = path_elements[1]

        if len(path_elements) < 2 or \
                (len(path_elements) == 2 and contest_name != "create"):
            self.redirect_to_settings(self,
                                      os.path.join(self.request.path,
                                                   "settings"))
            return
        elif len(path_elements) == 2 and contest_name == "create":
            self.render("contest_create.html")
            return
        elif len(path_elements) >= 4:
            self.redirect("..")
            return

        if path_elements[2] not in ["settings",
                                    "announcements",
                                    "questions",
                                    "ranking",
                                    "problems",
                                    "submissions",
                                    "user_tests",
                                    "users",
                                    "addusers"]:
            self.redirect_to_settings(self, "settings")
        render = path_elements[2]

        render = "contest_" + render
        """
        if render == "settings":
            render = "contest_settings"
        elif render == "problems":
            render = "contest_problems"
        elif render == "submissions":
            render = "contest_submissions"
        elif render == "user_tests":
            render = "contest_user_tests"
        elif render == "users":
            render = "contest_users"
        elif render == "ranking":
            render = "contest_ranking"
        """

        try:
            session = self.acquire_sql_session()
        except SQLAlchemyError:
            traceback.print_exc()
            raise HTTPError(500, 'Could not acquire database session.')

        try:
            contest = ContestRepository.get_by_name(session, contest_name)
            problems = ContestRepository.get_all_problems(session, contest.id)
        except SQLAlchemyError:
            traceback.print_exc()
            raise HTTPError(500, 'Error getting problems')

        if render == "contest_settings":
            contest = session.query(Contest) \
                .filter_by(name=contest_name) \
                .one()
            self.render(render + ".html",
                        last_path=path_elements[2],
                        contest_id=contest_name,
                        contest_name=contest.name,
                        contest_description=contest.description,
                        contest_type=self.type_format(contest.type),
                        virtual_contest=self.checkbox_format(contest.virtual),
                        allow_download=self
                        .checkbox_format(contest.submission_download_allowed),
                        allow_questions=self
                        .checkbox_format(contest.allow_questions),
                        allow_usertest=self
                        .checkbox_format(contest.allow_user_test),
                        start_time=self.time_format(contest.start_time),
                        end_time=self.time_format(contest.end_time),
                        restricted_ip=contest.restricted_ip,
                        max_submissions=contest.max_submissions,
                        max_user_tests=contest.max_user_test,
                        submission_delay=contest.min_submission_interval,
                        user_test_delay=contest.min_user_test_interval,
                        )
            session.close()
            return

        session.close()
        self.render(render + ".html",
                    last_path=path_elements[2],
                    contest=contest,
                    contest_id=contest_name,
                    problems=problems)

    @staticmethod
    def redirect_to_settings(self, path):
        self.redirect(path)

    @staticmethod
    def checkbox_format(val):
        if val:
            return "checked"
        return ""

    @staticmethod
    def type_format(val):
        if val == 1:
            return "Open"
        elif val == 2:
            return "Public"
        elif val == 3:
            return "Private"
        return "Open"

    @staticmethod
    def time_format(time_utc):
        calendar_time = \
            time.gmtime(time_utc)
        correct_time = \
            time.strftime('%m/%d/%Y %I:%M %p', calendar_time)
        return correct_time
