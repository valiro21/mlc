# coding=utf-8
"""Submissions Handler for BackendWebServer."""

from BackendServer.handlers.BaseHandler import BaseHandler

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>


class SubmissionsHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("submissions.html")
