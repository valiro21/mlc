"""LoginHandler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

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
        action = path_elements[-1]

        # Check if create is asked
        if action == 'create':
            self.render("problem_create.html")
            return

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        # Get problem name
        name = self.get_argument('name', None)

        if action == 'edit':
            if name is None:
                # If no name specified, redirect to create page
                self.redirect('/problem/create')
                session.close()
                return

            # Find problem in database
            try:
                problem = ProblemRepository.get_by_name(session, name)
            except:
                # If problem does not exist, redirect user to create it
                self.render('problem_create.html', problem_name=name)
                session.close()
                return

            self.render("problem_edit.html", problem=problem)
            session.close()
            return

        raise HTTPError(404, 'Not found')

    def post(self):
        print("POST to ProblemHandler")

        functions = {'create': getattr(self, 'create_problem'),
                     'edit': getattr(self, 'edit_problem')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404, 'Not found')

    def edit_problem(self):

        try:
            old_name = self.get_argument('old-name')
            new_name = self.get_argument('name')

            active_ds_id = self.get_argument('active-dataset-id', None)

            new_description = self.get_argument('description')
            new_statements = self.request.files.get('statements', [])
            new_attachments = self.request.files.get('attachments', [])
        except:
            raise HTTPError(400)

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        try:
            problem = ProblemRepository.get_by_name(session, old_name)

            problem.name = new_name
            problem.description = new_description

            if active_ds_id is None and len(problem.datasets) > 0:
                active_ds_id = problem.datasets[0].id

            problem.active_dataset_id = active_ds_id

            self.set_statements_and_attachments(new_attachments,
                                                new_statements,
                                                problem)
            session.commit()
        except Exception as e:
            raise HTTPError(500, 'Database error or invalid arguments.')

        self.redirect('/problem/edit?name=' + problem.name)
        session.close()

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
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        try:
            new_problem = Problem(name=name, description=description)
            session.add(new_problem)
            session.commit()
        except SQLAlchemyError as e:
            print(e)

            msg = repr(e).replace('\\n', '\n')  # to output message properly
            self.render('problem_create.html', error_msg=msg)
            return

        print('Created problem ' + name)
        self.redirect('/problem/edit?name=' + name)
        session.close()
