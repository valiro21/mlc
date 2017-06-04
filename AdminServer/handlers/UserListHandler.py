# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

from tornado.web import HTTPError

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.User import User


class UserListHandler(BaseHandler):
    def get(self):

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        try:
            query = session.query(User)
            users = session.execute(query)
            user_list = users.fetchall()
        except:
            raise HTTPError(500, 'Database error')

        self.render("user_list.html", users=user_list)
        session.close()
