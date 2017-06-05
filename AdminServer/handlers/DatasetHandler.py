"""Dataset Handler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
import os
import traceback
import zipfile
from io import BytesIO

import tornado.web
from sqlalchemy.exc import SQLAlchemyError
from tornado.web import HTTPError, MissingArgumentError

from AdminServer.handlers.BaseHandler import BaseHandler
from DB import Testcase
from DB.Entities import Dataset
from DB.Repositories import DatasetRepository


class DatasetHandler(BaseHandler):
    """Handler for working with datasets."""

    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self):
        print("GET to DatasetHandler")

        functions = {'edit': getattr(self, 'edit_dataset')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404)

    def edit_dataset(self):
        try:
            id = int(self.get_argument('id'))
            session = self.acquire_sql_session()
            dataset = DatasetRepository.get_by_id(session, id)
        except MissingArgumentError:
            raise HTTPError(404, 'No id specified')
        except SQLAlchemyError:
            raise HTTPError(500, 'Database error, could not find specified id')
        except:
            raise HTTPError(500, 'Shit happened')

        self.render('dataset_edit.html', dataset=dataset)
        session.close()

    @tornado.web.authenticated
    def post(self):
        print("POST to DatasetHandler")

        functions = {'create': getattr(self, 'create_dataset_post'),
                     'edit': getattr(self, 'edit_dataset_post'),
                     'delete': getattr(self, 'delete_dataset_post')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404)

    def create_dataset_post(self):

        print(self.request.files)

        # Get arguments from request
        try:
            problem_id = self.get_argument('problem-id')
            name = self.get_argument('name')
            time_limit = self.get_argument('time-limit')
            memory_limit = self.get_argument('memory-limit')

            stdin = self.get_argument('stdin', '')
            stdout = self.get_argument('stdout', '')
            # max_score = self.get_argument('max-score')

            testcases_info = self.request.files['testcases'][0]
            # testcases_name = testcases_info['filename']
            testcases_body = testcases_info['body']

        except Exception as e:
            traceback.print_exc()
            raise HTTPError(400)  # Bad request

        try:
            session = self.acquire_sql_session()
        except:
            traceback.print_exc()
            # TODO: handle error
            return

        try:
            # Create a new empty dataset (in order to get an ID)
            new_dataset = self.create_empty_dataset(memory_limit,
                                                    name,
                                                    problem_id,
                                                    time_limit,
                                                    stdin,
                                                    stdout,
                                                    session
                                                    )
            # Extract testcases_body
            extracted = self.extract_zip(testcases_body)

            # Go through files and construct testcases
            self.create_testcases(extracted, new_dataset, session)
            # Commit changes (add testcases)
            session.commit()
        except Exception as e:
            traceback.print_exc()
            session.rollback()
            raise HTTPError(400)

        self.redirect('/problem/' + new_dataset.problem.name)
        session.close()

    def create_testcases(self, extracted, new_dataset, session):
        if extracted is None:
            return

        for filename in extracted.keys():
            if filename.endswith('.in'):
                base = os.path.splitext(filename)[0]
                in_file = extracted[base + '.in']
                ok_file = extracted[base + '.ok']

                new_testcase = Testcase(dataset_id=new_dataset.id,
                                        input_file=in_file,
                                        output_file=ok_file,
                                        codename=base)
                session.add(new_testcase)

    def create_empty_dataset(self,
                             memory_limit,
                             name,
                             problem_id,
                             time_limit,
                             stdin,
                             stdout,
                             session):
        # Create a new dataset with no testcases

        new_dataset = Dataset(name=name,
                              problem_id=problem_id,
                              time_limit=time_limit,
                              memory_limit=memory_limit,
                              stdin=stdin,
                              stdout=stdout)
        session.add(new_dataset)
        session.flush()  # Runs the insert, and sets the ID of the dataset
        return new_dataset

    def extract_zip(self, input_zip):
        if input_zip is None:
            return None

        zip_ref = zipfile.ZipFile(BytesIO(input_zip), 'r')
        return {name: zip_ref.read(name) for name in zip_ref.namelist()}

    def edit_dataset_post(self):
        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        try:
            id = int(self.get_argument('id'))
            new_name = self.get_argument('name')
            new_stdin = self.get_argument('stdin')
            new_stdout = self.get_argument('stdout')
            new_time_limit = self.get_argument('time-limit')
            new_memory_limit = self.get_argument('memory-limit')

            files = self.request.files

            testcases = files.get('testcases', None)
            if testcases is not None:
                testcases_info = testcases[0]
                testcases_body = testcases_info['body']
            else:
                testcases_body = None

            new_in = files.get('input', None)
            new_out = files.get('output', None)
        except:
            raise HTTPError(400, 'Arguments specified incorrectly.')

        try:
            dataset = DatasetRepository.get_by_id(session, id)
            dataset.name = new_name
            dataset.stdin = new_stdin
            dataset.stdout = new_stdout

            dataset.time_limit = new_time_limit
            dataset.memory_limit = new_memory_limit

            if (new_in is not None) or (new_out is not None):
                if (new_in is None) or (new_out is None):
                    raise HTTPError(400, 'Missing input/output '
                                         'for single testcase')
                new_testcase = Testcase(dataset_id=dataset.id,
                                        input_file=new_in[0]['body'],
                                        output_file=new_out[0]['body'])
                session.add(new_testcase)

            extracted = self.extract_zip(testcases_body)
            self.create_testcases(extracted, dataset, session)

            session.commit()
        except SQLAlchemyError as e:
            raise HTTPError(400, 'Error modifying dataset.')

        self.redirect('/dataset/edit?id=' + str(id))
        session.close()

    def delete_dataset_post(self):
        try:
            session = self.acquire_sql_session()
        except:
            # TODO: handle error
            traceback.print_exc()
            return

        try:
            id = self.get_argument('id')
            session.query(Dataset).filter_by(id=id).delete()
            session.commit()

        except Exception as e:
            traceback.print_exc()
            raise HTTPError(400)

        finally:
            session.close()
