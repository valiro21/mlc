"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import os

from sqlalchemy.exc import SQLAlchemyError

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities import Problem


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

        if len(path_elements) < 2 or \
                (len(path_elements) == 2 and problem_id != "create"):
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
        print("POST to ProblemHandler")

        path_elements = [x for x in self.request.path.split("/") if x]

        if (path_elements[-1] == 'create'):
            self.create_problem()
            return

    def create_problem(self):
        """Creates a problem with given name and description"""

        try:
            name = self.get_argument('name')
            description = self.get_argument('description')
        except Exception as e:
            print(e)
            self.render('problem_create.html', error_msg=e)
            return

        try:
            new_problem = Problem(name=name, description=description)
            self.session.add(new_problem)
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)

            msg = repr(e).replace('\\n', '\n')   # to output message properly
            self.render('problem_create.html', error_msg=msg)
            return

        print('Created problem ' + name)
        self.redirect('/problem/' + name)
