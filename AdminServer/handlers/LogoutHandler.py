"""Handler for logging out"""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from AdminServer.handlers.BaseHandler import BaseHandler
import tornado.web


class LogoutHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("admin")
        self.redirect("/")
