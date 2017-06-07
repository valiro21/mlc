"""BaseHandler for AdminServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

import tornado.web
from tornado.web import HTTPError
from DB import session_factory
from DB.Repositories import ContestRepository, \
    ProblemRepository, \
    UserRepository


class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler for tornado RequestHandler. Adds option for users."""

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("admin")

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def acquire_sql_session(self):
        return session_factory()

    def get_template_namespace(self):
        try:
            session2 = self.acquire_sql_session()
            sidebar_contests = ContestRepository.\
                get_all_contest_order_by_date(session2)
            sidebar_problems = ProblemRepository.get_all_problems(session2)
            sidebar_users = UserRepository.get_all(session2)
            session2.close()
        except:
            raise HTTPError(500)

        dict = super(BaseHandler, self).get_template_namespace()

        dict['sidebar_contests'] = sidebar_contests
        dict['sidebar_problems'] = sidebar_problems
        dict['sidebar_users'] = sidebar_users

        return dict
