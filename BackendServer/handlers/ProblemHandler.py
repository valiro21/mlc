# coding=utf-8
"""ProblemHandler for contestants."""

import os
from BackendServer.handlers.BaseHandler import BaseHandler
import tornado.web

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
from DB.Repositories import ProblemRepository


class ProblemHandler(BaseHandler):
    """Tornado handler for a problem."""
    def data_received(self, chunk):
        pass

    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        problem_name = path_elements[1]

        problem = ProblemRepository.get_by_name(self.session, problem_name)
        if problem is None:
            raise tornado.web.HTTPError(404)

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "statement"))
            return
        if len(path_elements) >= 4:
            self.redirect("..")
            return

        if path_elements[2] == 'pdf':
            self.write(problem.statements[0])

        if path_elements[2] not in ["statement",
                                    "submissions",
                                    "editorial",
                                    "comments"]:
            self.redirect("statement")

        self.render("problem_" +
                    path_elements[2] +
                    ".html", problem=problem)
