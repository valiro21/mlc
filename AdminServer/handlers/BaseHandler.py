"""BaseHandler for AdminServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler for tornado RequestHandler. Adds option for users."""

    def get_current_user(self):
        return self.get_secure_cookie("user")
