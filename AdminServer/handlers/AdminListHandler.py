"""AdminListHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import tornado.web
from tornado.web import HTTPError
from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.Admin import Admin
from DB.Entities.Permission import Permission


class AdminListHandler(BaseHandler):
    """AdminListHandler for admins."""

    @tornado.web.authenticated
    def get(self):

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        try:
            query = session.query(Admin)
            admins = session.execute(query)
            admin_list = admins.fetchall()
        except:
            raise HTTPError(500, 'Database error')

        try:
            query = session.query(Permission)
            permissions = session.execute(query)
        except:
            raise HTTPError(500, 'Database error')

        self.render("admin_list.html",
                    admins=admin_list,
                    permissions=permissions)

    def post(self):
        # TODO
        pass
