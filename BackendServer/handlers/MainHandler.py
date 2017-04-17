# coding=utf-8
"""RootHandler for BackendWebServer."""

import tornado.web

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

class MainHandler(tornado.web.RequestHandler):
    """Root Handler for BackendWebServer."""

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("main.html")
