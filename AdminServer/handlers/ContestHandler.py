"""ContestHandler for AdminServer. This is used for updating contests. """

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
import calendar
import os
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from AdminServer.handlers import BaseHandler
from DB.Contest import Contest


class ContestHandler(BaseHandler.BaseHandler):
    """Handler for login."""

    def data_received(self, chunk):
        pass

    def post(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        contest_id = path_elements[1]
        if len(path_elements) == 2 and contest_id == "create":
            contest_name = self.get_argument('contest_name')
            start_date_string = self.get_argument('start_date')
            print(start_date_string)
            start_date = \
                datetime.strptime(start_date_string, '%m/%d/%Y %I:%M %p')
            start_date_utc = calendar.timegm(start_date.timetuple())
            end_date_string = self.get_argument('end_date')
            end_date = datetime.strptime(end_date_string, '%m/%d/%Y %I:%M %p')
            end_date_utc = calendar.timegm(end_date.timetuple())
            try:
                new_contest = Contest(name=contest_name,
                                      description='',
                                      start_time=start_date_utc,
                                      end_time=end_date_utc)
                self.session.add(new_contest)
                self.session.commit()
            except SQLAlchemyError as e:
                self.redirect("contest_create.html")
                print(e)
                return
            self.redirect(os.path.join(self.request.path, "settings"))
            return
        elif len(path_elements) == 3 and path_elements[2] == 'setting':
            contest_name = self.get_argument('contest_name')
            contest_description = self.get_argument('contest_description')
            contest_type = \
                self.get_argument('contest_type')
            contest_virtual = \
                self.get_argument('contest_virtual')
            contest_allow_download = \
                self.get_argument('contest_allow_download')
            contest_allow_questions = \
                self.get_argument('contest_allow_questions')
            contest_allow_usertest = \
                self.get_argument('contest_allow_usertest')
            contest_restricted_ip = \
                self.get_argument('contest_restricted_ip')
            contest_start_time = \
                self.get_argument('contest_start_time')
            contest_end_time = \
                self.get_argument('contest_end_time')
            contest_timezone = \
                self.get_argument('contest_timezone')
            contest_max_submissions = \
                self.get_argument('contest_max_submissions')
            contest_max_user_tests = \
                self.get_argument('contest_max_user_tests')
            contest_submission_delay = \
                self.get_argument('contest_min_submission_interval')
            contest_user_test_delay = \
                self.get_argument('contest_min_user_test_interval')
            try:
                contest_old_name = path_elements[1]
                contest_table = self.session.query(Contest)
                contest_table.update(). \
                    where(contest_table.name == contest_old_name). \
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
                           time_zone=contest_timezone,
                           max_submissions=contest_max_submissions,
                           max_user_tests=contest_max_user_tests,
                           min_submission_interval=contest_submission_delay,
                           min_user_test_interval=contest_user_test_delay)
                self.session.commit()
            except SQLAlchemyError as e:
                print(e)
                self.redirect(os.path.join(self.request.path, "settings"))
                return
            self.redirect(os.path.join(self.request.path, "settings"))

    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        if len(path_elements) == 1:
            self.render("contests.html")
            return
        contest_id = path_elements[1]

        if len(path_elements) < 2 or \
                (len(path_elements) == 2 and contest_id != "create"):
            self.redirect(os.path.join(self.request.path, "settings"))
            return
        elif len(path_elements) == 2 and contest_id == "create":
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
                                    "users"]:
            self.redirect("settings")
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

        self.render(render + ".html",
                    last_path=path_elements[2],
                    contest_id=contest_id)
