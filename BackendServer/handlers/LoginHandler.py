"""Handler for Login Form"""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

from BackendServer.handlers.BaseHandler import BaseHandler
from DB.Entities import User
from sqlalchemy.sql import or_
import bcrypt


class LoginHandler(BaseHandler):
    """Handler that listens for POST requests on /login"""
    def data_received(self, chunk):
        pass

    def post(self):
        username = self.get_argument('login_username', '')
        password = self.get_argument('login_password', '')

        """Check the username and password from the post request"""
        if not username:
            login_response = 'Please enter your username/email.'
            self.write(login_response)
            return

        if not password:
            login_response = 'Please enter your password.'
            self.write(login_response)
            return

        try:
            session = self.acquire_sql_session()
        except:
            login_response = 'Could not acquire db connection'
            self.write(login_response)
            return


        try:
            """Check if the user exists and grab his hashed password to compare it later"""
            query = session.query(User.password)\
                .filter(or_(User.username == username, User.email == username))

            db_pass = session.execute(query).first()

            """User does not exist"""
            if not db_pass:
                login_response = 'Invalid credentials.'
                self.write(login_response)
                return

            """Hash the password given and compare it with the stored hash"""
            if bcrypt.checkpw(password.encode('utf8'),
                              db_pass[0].encode('utf8')):
                db_user = session.query(User)\
                    .filter(or_(User.username == username,
                                User.email == username))\
                    .one_or_none()

                """Check whether the user needs to confirm his account or not"""
                if db_user is not None:
                    if db_user.confirmation_token is not None:
                        login_response = 'Account is not confirmed.'
                    else:
                        self.set_secure_cookie("user", db_user.username)
                        login_response = 'Logged in.'

                else:
                    login_response = 'Unexpected error.'

            else:
                login_response = 'Invalid credentials.'
        except Exception as err:
            print(err)
            login_response = 'A database error has occurred.'
        finally:
            session.close()

        self.write(login_response)
        return
