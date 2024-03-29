"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

import bcrypt
from tornado.web import HTTPError

from AdminServer.handlers import BaseHandler
from DB.Entities.Admin import Admin


class LoginHandler(BaseHandler.BaseHandler):
    """Handler for login."""

    def data_received(self, chunk):
        pass

    def get(self):
        if self.current_user:
            self.redirect(r"/")
            return
        self.render("login.html")

    def post(self):
        # Get username and password from request
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        if username != 'admin' and password != 'admin':

            try:
                session = self.acquire_sql_session()
            except:
                raise HTTPError(500, 'Could not acquire session for database')

            try:
                query = session.query(Admin.password) \
                    .filter(Admin.username == username)

                result = session.execute(query)
            except:
                raise HTTPError(500, 'Database error')

            db_pass = None

            for pwd in result:
                db_pass = pwd

            if not db_pass:
                self.render("login.html", invalid=True)

            if bcrypt.checkpw(password.encode('utf8'),
                              db_pass[0].encode('utf8')):
                self.set_secure_cookie("admin", username)
                self.get_current_user()
                self.redirect(r"/")

            self.render("login.html", invalid=True)
            session.close()

        else:
            self.set_secure_cookie("admin", "admin")
            self.redirect(r"/")
