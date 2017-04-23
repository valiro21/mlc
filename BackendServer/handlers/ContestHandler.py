# coding=utf-8
"""Contest Handler for contest page."""

import tornado.web
import os

# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>


class ContestHandler(tornado.web.RequestHandler):
    """Tornado handler for a contest."""
    def data_received(self, chunk):
        pass

    def get(self):

        path_elements = [x for x in self.request.path.split("/") if x]
        contest_id = path_elements[1]

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "problems"))
            return
        if len(path_elements) >= 4:
            self.redirect("..")
            return

        if path_elements[2] not in ["problems",
                                    "submit",
                                    "mysubmissions",
                                    "submissions",
                                    "standings"]:
            self.redirect("problems")

        self.render("contest_" + path_elements[2] + ".html", contest_id=contest_id)
