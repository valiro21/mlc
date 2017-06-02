# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.Admin import Admin
import bcrypt


class CreateAdminHandler(BaseHandler):
    """Handler for creating a new admin"""

    def post(self):
        name = self.get_argument('name', '')
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        password_confirm = self.get_argument('password_confirmation', '')

        if not name:
            register_response = 'Please enter a name.'

        elif not username:
            register_response = 'Please enter an username.'

        elif not email:
            register_response = 'Please enter an email.'

        elif not password:
            register_response = 'Please enter a password.'

        elif not password_confirm:
            register_response = 'Please confirm the password.'

        elif password != password_confirm:
            register_response = 'Your passwords differ.'

        else:
            register_response = 'registered'

        new_admin = Admin(
            username=username,
            name=name,
            email=email,
            password=bcrypt.hashpw(password.encode('utf8'),
                                   bcrypt.gensalt()).decode('utf8')
        )

        self.session.add(new_admin)

        self.session.commit()

        self.write(register_response)

        self.redirect(r"/admin_list")
