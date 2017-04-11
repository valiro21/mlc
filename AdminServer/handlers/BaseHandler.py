"""BaseHandler for AdminServer."""

import tornado.web

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler for tornado RequestHandler. Adds option for users."""
    def get_current_user(self):
        return self.get_secure_cookie("user")
