# coding=utf-8
"""Submissions Handler for BackendWebServer."""

import tornado.web

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

class SubmissionsHandler(tornado.web.RequestHandler): 

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("submissions.html")
