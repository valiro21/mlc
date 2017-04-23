"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from AdminServer.handlers import BaseHandler


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
        username = self.get_argument("username")
        password = self.get_argument("password")
        if username != "admin" or password != "admin":
            self.render("login.html", invalid=True)
        self.set_secure_cookie("user", "admin")
        self.redirect(r"/")
