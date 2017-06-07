# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
import tornado.web
import bcrypt

from tornado.web import HTTPError
from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.User import User


class EditUserHandler(BaseHandler):
    """
    Handler for editing a specific user
    """

    @tornado.web.authenticated
    def get(self):
        self.redirect("r/")

    @tornado.web.authenticated
    def post(self):
        username = self.get_argument('username', '')
        new_first_name = self.get_argument('first_name', '')
        new_last_name = self.get_argument('last_name', '')
        new_email = self.get_argument('email', '')
        new_pass = self.get_argument('password', '')
        new_pass_confirmation = self.get_argument('password_confirmation', '')

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        try:
            selected_user = session.query(User)\
                .filter(User.username == username)\
                .one_or_none()

            if new_first_name != '':
                selected_user.firstName = new_first_name

            if new_last_name != '':
                selected_user.lastName = new_last_name

            if new_email != '':
                selected_user.email = new_email

            if new_pass == new_pass_confirmation and new_pass != '':
                selected_user.password = \
                    bcrypt.hashpw(new_pass.encode('utf8'),
                                  bcrypt.gensalt()).decode('utf8')

            session.commit()
        except:
            raise HTTPError(500, 'Database error')

        self.redirect(r"/user_list")
        session.close()
