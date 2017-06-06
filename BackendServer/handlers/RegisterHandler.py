"""Handler for the register form"""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from BackendServer.handlers.BaseHandler import BaseHandler
from Common.scripts.Mailer import send_email
from DB.Entities import User
import bcrypt
import hashlib
import os


class RegisterHandler(BaseHandler):
    """
    Handler that listens for POST requests on '/register' and
    creates a user if the POST request is valid.
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

            """Generate confirmation token to be sent to the email"""

            token = hashlib.sha1(os.urandom(128)).hexdigest()

            new_user = User(
                username=username,
                firstName=first_name,
                email=email,
                lastName=last_name,
                password=bcrypt.hashpw(password.encode('utf8'),
                                       bcrypt.gensalt()).decode('utf8'),
                confirmation_token=token
            )

            session = self.acquire_sql_session()
            session.add(new_user)
            session.commit()

            message = self.request.protocol + "://" \
                + self.request.host + "/confirm/" + token

            send_email(email, "MLC Confirmation Link", message, username)

        self.write(register_response)
