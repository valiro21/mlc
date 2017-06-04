"""Handler for the register form"""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
import traceback

from tornado.web import HTTPError

from BackendServer.handlers.BaseHandler import BaseHandler
from DB.Entities import User
import bcrypt


class CreateUserHandler(BaseHandler):
    """
    Handler that listens for POST requests on '/create_user' and
    creates a user if POST request is valid
    """

    def data_received(self, chunk):
        pass

    def post(self):
        first_name = self.get_argument('first_name', '')
        last_name = self.get_argument('last_name', '')
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        password_confirm = self.get_argument('password_confirmation', '')

        if not first_name:
            register_response = 'Please enter your first name.'

        elif not last_name:
            register_response = 'Please enter your first name.'

        elif not username:
            register_response = 'Please enter your username.'

        elif not email:
            register_response = 'Please enter your email.'

        elif not password:
            register_response = 'Please enter your password.'

        elif not password_confirm:
            register_response = 'Please confirm your password.'

        elif password != password_confirm:
            register_response = 'Your passwords differ.'

        else:
            register_response = 'registered'
            new_user = User(
                username=username,
                firstName=first_name,
                email=email,
                lastName=last_name,
                password=bcrypt.hashpw(password.encode('utf8'),
                                       bcrypt.gensalt()).decode('utf8')
            )

            try:
                session = self.acquire_sql_session()
            except:
                traceback.print_exc()
                # TODO: handle error
                return

            try:
                session.add(new_user)
                session.commit()
            except:
                raise HTTPError(500, 'An error has occured')
            finally:
                session.close()

        self.write(register_response)
