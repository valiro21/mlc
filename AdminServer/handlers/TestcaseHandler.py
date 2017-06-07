"""Dataset Handler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
import traceback

import tornado.web
from sqlalchemy.exc import SQLAlchemyError
from tornado.web import HTTPError, MissingArgumentError

from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Repositories import TestcaseRepository


class TestcaseHandler(BaseHandler):
    """Handler for working with testcases."""

    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self):
        print("GET to TestcaseHandler")

        functions = {'view_input': getattr(self, 'view_input'),
                     'view_output': getattr(self, 'view_output')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404)

    @tornado.web.authenticated
    def post(self):

        functions = {'delete': getattr(self, 'delete_testcase')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404)

    def delete_testcase(self):

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire database session.')

        try:
            id = int(self.get_argument('id'))

            try:
                TestcaseRepository.delete_by_id(session, id)
            except SQLAlchemyError:
                traceback.print_exc()
                raise HTTPError(400, 'Testcase with specified id '
                                     'does not exist.')
            session.commit()
        except MissingArgumentError as e:
            traceback.print_exc()
            self.set_status(400)
            self.write('Id not specified in request.')
            return
        except SQLAlchemyError as e:
            traceback.print_exc()
            self.set_status(500)
            self.write('Databse error occured.')
            return
        except HTTPError:
            raise
        except:
            traceback.print_exc()
            self.set_status(500)
            self.write('Unexpected error occured.')
            return
        finally:
            session.close()

        self.write('Success!')

    def view_input(self):
        try:
            id = int(self.get_argument('id'))
            session = self.acquire_sql_session()
            try:
                testcase = TestcaseRepository.get_by_id(session, id)
            except SQLAlchemyError:
                raise HTTPError(400, 'Testcase with specified '
                                     'id does not exist.')

        except MissingArgumentError:
            raise HTTPError(404, 'No id specified.')
        except HTTPError:
            raise
        except SQLAlchemyError:
            raise HTTPError(500, 'Database error, could not '
                                 'find specified id.')
        except:
            raise HTTPError(500, 'Unexpected error')

        self.write(testcase.input_file)
        session.close()

    def view_output(self):
        try:
            id = int(self.get_argument('id'))
            session = self.acquire_sql_session()
            testcase = TestcaseRepository.get_by_id(session, id)
        except MissingArgumentError:
            raise HTTPError(404, 'No id specified')
        except SQLAlchemyError:
            raise HTTPError(500, 'Database error, could not find specified id')
        except:
            raise HTTPError(500, 'Shit happened')

        self.write(testcase.output_file)
        session.close()
