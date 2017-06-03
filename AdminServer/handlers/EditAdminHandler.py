# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
import tornado.web

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.Permission import Permission
from DB.Entities.Admin import Admin
from DB.Entities.Admin_Permission import AdminPermission


class EditAdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.redirect("r/")

    @tornado.web.authenticated
    def post(self):
        new_name = self.get_argument('name', '')
        new_email = self.get_argument('email', '')
        new_pass = self.get_argument('password', '')
        new_pass_confirmation = self.get_argument('password_confirmation', '')
        new_permissions = []

        querry = self.session.query(Permission)
        permission_list = self.session.execute(querry)

