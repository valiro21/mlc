"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
import os

from AdminServer.handlers.BaseHandler import BaseHandler


class ProblemHandler(BaseHandler):
    """Handler for login."""
    def data_received(self, chunk):
        pass

    def get(self):
        path_elements = [x for x in self.request.path.split("/") if x]
        if len(path_elements) == 1:
            self.render("problem_list.html")
            return
        problem_id = path_elements[1]

        if len(path_elements) < 2 or (len(path_elements) == 2 and
                                      problem_id != "create"):
            self.redirect(os.path.join(self.request.path, "edit"))
            return
        elif len(path_elements) == 2 and problem_id == "create":
            self.render("problem_create.html")
            return
        elif len(path_elements) >= 4:
            self.redirect("..")
            return

        self.render("problem_edit.html",
                    last_path=path_elements[2],
                    problem_id=problem_id)

    def post(self):
        # to do
        self.render('problem_edit.html')
        pass
