# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
import smtplib

from BackendServer.handlers.BaseHandler import BaseHandler
from DB.Entities.User import User
from DB.Entities.RecoveryToken import RecoveryToken
from Common.scripts.Mailer import send_email
import hashlib
import os
import datetime


class RecoveryHandler(BaseHandler):

    def get(self):

        path_elements = [x for x in self.request.path.split("/") if x]

        if len(path_elements) < 2:
            self.redirect(r"/")

        token = path_elements[1]

        self.render("reset_password.html", token=token)

    def post(self):
        path_elements = [x for x in self.request.path.split("/") if x]

        if len(path_elements) < 2:
            self.redirect(r"/")

        token = path_elements[1]

        if token == "send_email":

            email = self.get_argument('recovery_email', '')

            if email == '':
                response = 'Invalid email'
                self.write(response)
                return

            try:
                session = self.acquire_sql_session()
            except:
                response = 'Could not acquire db connection'
                self.write(response)
                return

            expiration_date = datetime.datetime.now()
            expiration_date = expiration_date + datetime.timedelta(minutes=30)

            query = session.query(User)\
                .filter(User.email == email).one_or_none()

            if query is not None:
                existing_token = session.query(RecoveryToken)\
                    .filter(RecoveryToken.user_id == query.id).one_or_none()

                if existing_token is not None:
                    session.delete(existing_token)

                token = hashlib.sha1(os.urandom(128)).hexdigest()
                recovery_token = RecoveryToken(
                    user_id=query.id,
                    recovery_token=token,
                    expiration_date=expiration_date
                )

                session.add(recovery_token)
                session.commit()
                message = self.request.protocol \
                    + "://" \
                    + self.request.host \
                    + "/recovery/" \
                    + token

                message = "To reset your password please " \
                          + "access the following link:\n" + message

                send_email(email, "MLC Recovery link", message, query.username)

                response = 'Mail sent.'
                self.write(response)
                return

            else:
                response = "Invalid email"

            self.write(response)
            return

        else:
            token = self.get_argument('token', '')
            # password = self.get_argument('password', '')
            # password_confirm = self.get_argument('password_confirm', '')

            try:
                session = self.acquire_sql_session()
            except:
                response = 'Could not acquire db connection'
                self.write(response)
                return

            query = session.query(RecoveryToken)\
                .filter(RecoveryToken.recovery_token == token)\
                .one_or_none()

            # user = session.query(User)\
            #    .filter(User.id == query.user_id).one_or_none()
