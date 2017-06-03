# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import tornado.web

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.User import User


class UserListHandler(BaseHandler):

    def get(self):
        query = self.session.query(User)

        users = self.session.execute(query)

        user_list = []

        for user in users:
            user_list.append(user)

        self.render("user_list.html", users=user_list)
