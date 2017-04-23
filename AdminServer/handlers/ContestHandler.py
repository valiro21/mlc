"""ContestHandler for AdminServer. This is used for updating contests. """

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import tornado

from AdminServer.handlers import BaseHandler


class ContestHandler(BaseHandler.BaseHandler):
    """Handler for login."""
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self):
        self.render("contest.html")
