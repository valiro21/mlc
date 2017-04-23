# coding=utf-8
"""ProblemHandler for contestants."""

import tornado.web
import os

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>


class ProblemHandler(tornado.web.RequestHandler):
    """Tornado handler for a problem."""
    def data_received(self, chunk):
        pass

    def get(self):

        path_elements = [x for x in self.request.path.split("/") if x]
        problem_id = path_elements[1]

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "statement"))
            return
        if len(path_elements) >= 4:
            self.redirect("..")
            return

        if path_elements[2] not in ["statement",
                                    "submissions",
                                    "editorial",
                                    "comments"]:
            self.redirect("statement")

        self.render(path_elements[2] + ".html", problem_id=problem_id)
