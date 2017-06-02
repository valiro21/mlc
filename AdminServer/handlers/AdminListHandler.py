"""AdminListHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import tornado
from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.Admin import Admin
from DB.Entities.Permission import Permission


class AdminListHandler(BaseHandler):
    """AdminListHandler for admins."""

    @tornado.web.authenticated
    def get(self):
        querry = self.session.query(Admin)

        admins = self.session.execute(querry)

        admin_list = []

        for admin in admins:
            admin_list.append(admin)

        querry = self.session.query(Permission)

        permissions = self.session.execute(querry)

        self.render("admin_list.html", admins=admin_list, permissions=permissions)

    def post(self):
        # to do
        pass
