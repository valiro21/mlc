# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

from AdminServer.handlers.BaseHandler import BaseHandler


class EditAdminHandler(BaseHandler):

    def get(self):
        self.redirect("r/")

    def post(self):
        pass
