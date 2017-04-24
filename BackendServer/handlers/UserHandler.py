# coding=utf-8
"""UserHandler for contestants."""

import tornado.web
import os

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>


class UserHandler(tornado.web.RequestHandler):
    """Tornado handler for a problem."""
    def data_received(self, chunk):
        pass

    def get(self):

        path_elements = [x for x in self.request.path.split("/") if x]
        user_id = path_elements[1]

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

        self.render(path_elements[2] + ".html", user_id=user_id)
