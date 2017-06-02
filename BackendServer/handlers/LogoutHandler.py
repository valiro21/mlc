"""Handler for logging out"""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

from BackendServer.handlers.BaseHandler import BaseHandler


class LogoutHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")
