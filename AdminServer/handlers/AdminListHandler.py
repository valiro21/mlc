"""AdminListHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import tornado

from AdminServer.handlers.BaseHandler import BaseHandler


class AdminListHandler(BaseHandler):
    """AdminListHandler for admins."""

    @tornado.web.authenticated
    def get(self):
        self.render("admin_list.html")

    def post(self):
        # to do
        pass
