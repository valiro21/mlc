"""BaseHandler for BackendServer."""

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import tornado.web
from DB import session_factory


class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler for tornado RequestHandler. Adds option for users."""

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if isinstance(user, str):
            return user
        if isinstance(user, bytearray) or isinstance(user, bytes):
            return user.decode()
        return user

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def acquire_sql_session(self):
        return session_factory()
