# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
import tornado

from AdminServer.handlers.BaseHandler import BaseHandler


class EditAdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.redirect("r/")

    @tornado.web.authenticated
    def post(self):
        pass
