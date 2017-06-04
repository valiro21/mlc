"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import os

import tornado.web
from sqlalchemy.exc import SQLAlchemyError
from tornado.web import HTTPError

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities import Problem
from DB.Repositories import ProblemRepository


class ProblemHandler(BaseHandler):
    """Handler for problem pages."""

    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
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
        problem = self.session.query(Problem) \
            .filter_by(name=problem_name) \
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

        print(self.request.files)

        try:
            old_name = self.get_argument('old-name')
            new_name = self.get_argument('name')
            new_description = self.get_argument('description')
            new_statements = self.request.files.get('statements', [])
            new_attachments = self.request.files.get('attachments', [])
        except:
            raise HTTPError(400)

        problem = ProblemRepository.get_by_name(self.session, old_name)

        problem.name = new_name
        problem.description = new_description

        self.set_statements_and_attachments(new_attachments,
                                            new_statements,
                                            problem)

        self.session.commit()
        print(problem.statement_names)

    def set_statements_and_attachments(self,
                                       new_attachments,
                                       new_statements,
                                       problem):
        statement_names = [st['filename'] for st in new_statements]
        attachment_names = [at['filename'] for at in new_attachments]
        statement_bodies = [st['body'] for st in new_statements]
        attachment_bodies = [at['body'] for at in new_attachments]

        st_temp_names = problem.statement_names + statement_names
        at_temp_names = problem.attachment_names + attachment_names
        st_temp_bodies = problem.statements + statement_bodies
        at_temp_bodies = problem.attachments + attachment_bodies

        problem.statement_names = st_temp_names
        problem.attachment_names = at_temp_names
        problem.statements = st_temp_bodies
        problem.attachments = at_temp_bodies

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

            msg = repr(e).replace('\\n', '\n')  # to output message properly
            self.render('problem_create.html', error_msg=msg)
            return

        print('Created problem ' + name)
        self.redirect('/problem/' + name)
