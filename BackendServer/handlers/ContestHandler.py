# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

# coding=utf-8
"""Contest Handler for contest page."""
import calendar
import os
import time
import traceback
from datetime import datetime
from sqlalchemy import update, desc
from sqlalchemy.exc import SQLAlchemyError
from tornado.httpclient import HTTPError

from BackendServer.handlers.BaseHandler import BaseHandler
from BackendServer.handlers.SubmissionsHandler import PrettyWrap

from DB import Participation, Contest
from DB.Entities import Submission, Problem, User
from DB.Entities.ContestPermissions import ContestPermissions
from DB.Repositories import ContestRepository, UserRepository, \
    SubmissionRepository
from DB.Repositories.ContestPermissionsRepository \
    import ContestPermissionsRepository
from DB.Repositories.ParticipacionRepository import ParticipationRepository


class ContestHandler(BaseHandler):
    """Tornado handler for a user contest."""

    def data_received(self, chunk):
        pass

    def post(self):
        """
        Handle for the post methods done on /contest/*
        Accepted operations:
            1. register: registers the current user to the current contest
            2. creatv: creates a virtual contest for the current user
            3. settingsv: provides setting for the contest if the user
                        has permission
        """
        path_elements = [x for x in self.request.path.split("/") if x]
        if len(path_elements) == 2:
            operation_type = path_elements[1]
        else:
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
        elif operation_type == 'createv':
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
            except SQLAlchemyError:
                traceback.print_exc()
                raise HTTPError(500, 'Could not acquire database session.')

            try:
                new_contest = Contest(name=contest_name,
                                      description='',
                                      start_time=start_date_utc,
                                      end_time=end_date_utc,
                                      virtual=True)
                session.add(new_contest)
                session.commit()
                user_name = self.get_current_user()

                if user_name is None:
                    self.render('you_must_be_logged.html')
                    return

                user = UserRepository.get_by_name(session, user_name)
                contest = ContestRepository.get_by_name(session, contest_name)
                new_permission = ContestPermissions(user_id=user.id,
                                                    contest_id=contest.id)
                session.add(new_permission)
                session.commit()
            except SQLAlchemyError as e:
                self.redirect("create")
                print(e)
                return

            self.redirect(contest_name + "/settingsv")
            session.close()
            return
        elif operation_type == 'settingsv':
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
                self.redirect_to_settings(self, "settingsv")
                return
            self.redirect("problems")
            session.close()

        self.redirect("contest_done_register")

    def get(self):
        """
        Handle for the get methods done on /contest/*
        Accepted pages:
            "problems", "submit", "mysubmissions", "submissions",
            "standings", "createv", "problemsv", "settingsv"
        """
        path_elements = [x for x in self.request.path.split("/") if x]
        contest_name = path_elements[1].replace('%20', ' ')

        if path_elements[1] == "createv":
            self.render("contest_" +
                        path_elements[1] + ".html")
            return
        session = self.acquire_sql_session()
        contest = ContestRepository.get_by_name(session, contest_name)

        problems = ContestRepository.get_all_problems(session, contest.id)

        for problem in problems:
            print(problem)

        if contest.type == 3:
            user_name = self.get_current_user()

            if user_name is None:
                self.render('you_must_be_logged.html')
                return

            user = UserRepository.get_by_name(session, user_name)

            ok = ParticipationRepository. \
                verif_participation(session, user.id, contest.id)

            if ok is False:
                self.redirect('..')
                return

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "problems"))
            return

        if path_elements[2] == 'settingsv':
            session = self.acquire_sql_session()
            contest = ContestRepository.get_by_name(session, contest_name)
            user_name = self.get_current_user()

            if user_name is None:
                self.render('you_must_be_logged.html')
                return

            user = UserRepository.get_by_name(session, user_name)
            ok = ContestPermissionsRepository\
                .check_permission(session, contest.id, user.id)
            if ok is False:
                self.render("contest_no_privileges.html",
                            contest_id=contest_name,
                            problems=problems
                            )
                return
            self.render("contest_" +
                        path_elements[2] + ".html",
                        last_path=path_elements[2],
                        contest_id=contest_name,
                        contest_name=contest.name,
                        contest_description=contest.description,
                        contest_type=self.type_format(contest.type),
                        allow_download=self
                        .checkbox_format(contest.
                                         submission_download_allowed),
                        allow_questions=self
                        .checkbox_format(contest.allow_questions),
                        allow_usertest=self
                        .checkbox_format(contest.allow_user_test),
                        start_time=self.time_format(contest.
                                                    start_time),
                        end_time=self.time_format(contest.end_time),
                        restricted_ip=contest.restricted_ip,
                        max_submissions=contest.max_submissions,
                        max_user_tests=contest.max_user_test,
                        submission_delay=contest.min_submission_interval,
                        user_test_delay=contest.min_user_test_interval,
                        )
            return

        if path_elements[2] == 'register':
            self.render("contest_register.html",
                        contest_name=contest_name,
                        contest_id=contest.id)
            return

        if len(path_elements) >= 4:
            self.redirect("..")
            return

        if path_elements[2] == 'submit' or path_elements[2] == 'mysubmissions':

            user_name = self.get_current_user()

            if user_name is None:
                self.render('you_must_be_logged.html')
                return

            user = UserRepository.get_by_name(session, user_name)

            ok = ParticipationRepository. \
                verif_participation(session, user.id, contest.id)

            if ok is False:
                self.render('contest_fail_non_registered.html')
                return

        if path_elements[2] not in ["problems",
                                    "submit",
                                    "mysubmissions",
                                    "submissions",
                                    "standings",
                                    "createv",
                                    "problemsv",
                                    "settingsv"]:
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

            self.render('contest_' + path_elements[2] + '.html',
                        contest_name=contest.name,
                        contest_id=contest.id,
                        submissions=return_list)
            return

        self.render("contest_" +
                    path_elements[2] + ".html",
                    contest_name=contest.name,
                    contest_id=contest.id,
                    problems=problems)

    @staticmethod
    def checkbox_format(val):
        """
        Formats a 1 or 0 to cheched format required by
        html form default values
        :param val:
        """
        if val:
            return "checked"
        return ""

    @staticmethod
    def type_format(val):
        """
        Converts stored type from datebase to the format required
        by the html from default values
        """
        if val == 1:
            return "Open"
        elif val == 2:
            return "Public"
        elif val == 3:
            return "Private"
        return "Open"

    @staticmethod
    def time_format(time_utc):
        """
        Converts stored data from datebase to the format required
        by the html from default values
        """
        calendar_time = \
            time.gmtime(time_utc)
        correct_time = \
            time.strftime('%m/%d/%Y %I:%M %p', calendar_time)
        return correct_time
