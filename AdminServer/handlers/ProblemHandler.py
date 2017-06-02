"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import os

from sqlalchemy.exc import SQLAlchemyError
from tornado.web import HTTPError

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities import Problem


class ProblemHandler(BaseHandler):
    """Handler for problem pages."""

    def data_received(self, chunk):
        pass

    def get(self):

        path_elements = [x for x in self.request.path.split("/") if x]
        if len(path_elements) == 1:
            self.render("problem_list.html")
            return
        problem_name = path_elements[1]

        if len(path_elements) < 2 or \
                (len(path_elements) == 2 and problem_name != "create"):
            self.redirect(os.path.join(self.request.path, "edit"))
            return
        elif len(path_elements) == 2 and problem_name == "create":
            self.render("problem_create.html")
            return
        elif len(path_elements) >= 4:
            self.redirect("..")
            return

        # Find problem (by name)
        problem = self.session.query(Problem)\
            .filter_by(name=problem_name)\
            .first()

        if problem is None:
            # Problem not existing, redirect to creation page
            self.render("problem_create.html", problem_name=problem_name)
            return

        self.render("problem_edit.html",
                    problem=problem)

    def post(self):
        print("POST to ProblemHandler")

        functions = {'create': getattr(self, 'create_problem'),
                     'edit': getattr(self, 'edit_problem')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404)

    def edit_problem(self):
        print('Not implemented!')
        pass

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
