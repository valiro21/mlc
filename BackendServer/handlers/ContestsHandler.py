# coding=utf-8
"""Contests Handler for BackendWebServer."""

import tornado.web

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

class ContestsHandler(tornado.web.RequestHandler):
   
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("contests.html")
