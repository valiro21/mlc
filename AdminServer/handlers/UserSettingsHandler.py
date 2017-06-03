"""UserSettingsHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import tornado.web

from AdminServer.handlers.BaseHandler import BaseHandler


class UserSettingsHandler(BaseHandler):
    """UserSettingsHandler for admins."""

    @tornado.web.authenticated
    def get(self):
        self.render("user_settings.html")

    def post(self):
        # to do
        self.render("user_settings.html")
        pass
