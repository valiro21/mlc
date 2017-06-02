"""Handler for logging out"""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

from AdminServer.handlers.BaseHandler import BaseHandler


class LogoutHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.clear_cookie("admin")
        self.redirect("/")
