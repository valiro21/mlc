# coding=utf-8
"""RootHandler for BackendWebServer."""

import tornado.web


# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

class MainHandler(tornado.web.RequestHandler):
    """Root Handler for BackendWebServer."""

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("main.html")
