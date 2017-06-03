"""SubmissionHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
import os

import tornado.web

from AdminServer.handlers.BaseHandler import BaseHandler


class SubmissionHandler(BaseHandler):
    """SubmissionHandler for viewing details about a submission."""

    @tornado.web.authenticated
    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]

        if len(path_elements) >= 3:
            self.redirect("..")
            return

        submission_id = path_elements[1]
        self.render("submission.html", id=submission_id)
