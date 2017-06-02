# coding=utf-8
"""Contests Handler for BackendWebServer."""

from BackendServer.handlers.BaseHandler import BaseHandler

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>


class ContestListHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.render("contest_list.html")
