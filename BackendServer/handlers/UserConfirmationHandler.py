# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from BackendServer.handlers.BaseHandler import BaseHandler
from DB.Entities import User, Participation
import time


class UserConfirmationHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]

        if len(path_elements) < 2:
            self.redirect(r"/")

        token = path_elements[1]

        try:
            session = self.acquire_sql_session()
        except:
            response = 'Could not acquire db connection'
            self.write(response)
            return

        query = session.query(User)\
            .filter(User.confirmation_token == token).one_or_none()

        if query is not None:
            query.confirmation_token = None
            self.set_secure_cookie("user", query.username)

            # Add default participation in archive
            participation = Participation(user_id=query.id, contest_id=1)
            session.add(participation)

            response = "Thank you for confirming " \
                       "your account. Enjoy your stay!"
            session.commit()

        else:
            response = "Invalid confirmation token"

        self.render("user_confirmation.html", response=response)
        time.sleep(5)
        self.redirect(r"/")
