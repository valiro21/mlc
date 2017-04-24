"""ContestHandler for AdminServer. This is used for updating contests. """

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
import os

import tornado

from AdminServer.handlers import BaseHandler


class ContestHandler(BaseHandler.BaseHandler):
    """Handler for login."""
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        if len(path_elements) == 1:
            self.render("contests.html")
            return
        contest_id = path_elements[1]

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "settings"))
            return
        if len(path_elements) >= 4:
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
