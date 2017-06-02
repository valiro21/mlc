"""Handler for Login Form"""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from BackendServer.handlers.BaseHandler import BaseHandler
from DB.User import User
from sqlalchemy.sql import or_
import bcrypt


class LoginHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        if not username:
            login_response = 'Please enter your username/email.'

        elif not password:
            login_response = 'Please enter you password.'

        querry = self.session.query(User.password)\
            .filter(or_(User.username == username, User.email == username))

        result = self.session.execute(querry)

        db_pass = None

        for pwd in result:
            db_pass = pwd

        if not db_pass:
            login_response = 'Invalid credentials.'

        if bcrypt.checkpw(password.encode('utf8'), db_pass[0].encode('utf8')):
            querry = self.session.query(User.username)\
                .filter(or_(User.username == username, User.email == username))

            result = self.session.execute(querry)

            db_user = None

            for usr in result:
                db_user = usr[0]

            if db_user:
                self.set_secure_cookie("user", db_user)
                self.get_current_user()
                login_response = 'Logged in.'

            else:
                login_response = 'Unexpected error.'

        else:
            login_response = 'Invalid credentials.'

        self.write(login_response)
