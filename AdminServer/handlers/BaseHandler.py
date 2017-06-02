"""BaseHandler for AdminServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import tornado.web
from DB import session_factory


class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler for tornado RequestHandler. Adds option for users."""

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("admin")

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.init_connection()

    def init_connection(self):
        """Initializes the database connection session variable"""
        self.session = session_factory()
