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
from DB.Repositories import DatasetRepository, ProblemRepository


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

            try:
                dataset = DatasetRepository.get_by_id(session, id)
            except:
                raise HTTPError(404, 'Specified id doesn\'t exist')

        except MissingArgumentError:
            raise HTTPError(404, 'No id specified')
        except SQLAlchemyError:
            raise HTTPError(500, 'Database error occured.')
        except HTTPError:
            raise
        except:
            raise HTTPError(500, 'Unexpected error occured')

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

        # Get arguments from request
        try:
            problem_id = int(self.get_argument('problem-id'))
            name = self.get_argument('name')
            time_limit = self.get_argument('time-limit')
            memory_limit = self.get_argument('memory-limit')

            # If received empty string, use database default
            try:
                time_limit = float(time_limit) if time_limit else None
                memory_limit = float(memory_limit) if memory_limit else None

                if not self.validate_time_memory(time_limit, memory_limit):
                    raise HTTPError(400, 'Invalid time limit or memory limit')

            except:
                raise HTTPError(400, 'Invalid time limit '
                                     'or memory limit format')
            stdin = self.get_argument('stdin', '')
            stdout = self.get_argument('stdout', '')

            files = self.request.files
            testcases = files.get('testcases', None)

            if testcases is not None:
                testcases_dict = testcases[0]
                testcases_body = testcases_dict['body']
            else:
                testcases_body = None

        except HTTPError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise HTTPError(400)  # Bad request

        try:
            session = self.acquire_sql_session()
        except:
            traceback.print_exc()
            raise HTTPError(500, 'Could not acquire database session.')

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
        except HTTPError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise HTTPError(400)
        finally:
            session.rollback()

        # Update the problem's default dataset
        try:
            ProblemRepository.update_default_dataset(session, problem_id)
            session.commit()
        except SQLAlchemyError:
            raise

        self.redirect('/problem/edit?name=' + new_dataset.problem.name)
        session.close()

    def create_testcases(self, extracted, new_dataset, session):
        if extracted is None:
            return

        for filename in extracted.keys():
            if filename.endswith('.in'):
                base = os.path.splitext(filename)[0]
                in_file = extracted[base + '.in']
                ok_file = extracted.get(base + '.ok', None)

                if ok_file is None:
                    raise HTTPError(400, 'Invalid zip file, corresponding '
                                         '.ok file does not exist.')

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

            new_time_limit = float(new_time_limit) \
                if new_time_limit else None
            new_memory_limit = float(new_memory_limit) \
                if new_time_limit else None

            if not self.validate_time_memory(new_time_limit, new_memory_limit):
                raise HTTPError(400, 'Invalid time limit or memory limit')

            files = self.request.files

            testcases = files.get('testcases', None)
            if testcases is not None:
                testcases_info = testcases[0]
                testcases_body = testcases_info['body']
            else:
                testcases_body = None

            new_in = files.get('input', None)
            new_out = files.get('output', None)
        except HTTPError:
            raise
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
            traceback.print_exc()
            raise HTTPError(500, 'Could not acquire database session.')

        try:
            id = int(self.get_argument('id'))

            dataset = DatasetRepository.get_by_id(session, id)
            problem_id = dataset.problem_id

            session.delete(dataset)
            session.commit()

            # Update the problem's default dataset
            try:
                ProblemRepository.update_default_dataset(session, problem_id)
                session.commit()
            except SQLAlchemyError:
                raise

        except Exception as e:
            traceback.print_exc()
            raise HTTPError(400)

        finally:
            session.close()

        self.write('Success!')

    def validate_time_memory(self, time, memory):
        return (time is None or 0 <= time <= 60) and \
               (memory is None or 0 <= memory <= 1024)
