"""Dataset Handler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
import os
import traceback
import zipfile

from io import StringIO, BytesIO
from sqlalchemy.exc import SQLAlchemyError
from tornado.web import HTTPError

from AdminServer.handlers.BaseHandler import BaseHandler
from DB import Testcase
from DB.Entities import Dataset


class DatasetHandler(BaseHandler):
    """Handler for working with datasets."""

    def data_received(self, chunk):
        pass

    def get(self):
        pass

    def post(self):
        print("POST to DatasetHandler")

        functions = {'create': getattr(self, 'create_complete_dataset'),
                     'edit': getattr(self, 'edit_dataset')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404)

    def create_complete_dataset(self):

        # Get arguments from request
        try:
            problem_id = self.get_argument('problem-id')
            name = self.get_argument('name')
            time_limit = self.get_argument('time-limit')
            memory_limit = self.get_argument('memory-limit')

            max_score = self.get_argument('max-score')

            testcases_info = self.request.files['testcases'][0]
            testcases_name = testcases_info['filename']
            testcases_body = testcases_info['body']

        except Exception as e:
            traceback.print_exc()
            raise HTTPError(400) # Bad request

        try:
            # Create a new empty dataset (in order to get an ID)
            new_dataset = self.create_empty_dataset(memory_limit,
                                                    name,
                                                    problem_id,
                                                    time_limit
                                                    )
            # Extract testcases_body
            extracted = self.extract_zip(testcases_body)

            # Go through files and construct testcases
            self.create_testcases(extracted, new_dataset)
            # Commit changes (add testcases)
            self.session.commit()
        except Exception as e:
            traceback.print_exc()
            self.session.rollback()
            raise HTTPError(400)

        self.redirect('/problem/' + new_dataset.problem.name)

    def create_testcases(self, extracted, new_dataset):
        for filename in extracted.keys():
            print(filename)
            if filename.endswith('.in'):
                base = os.path.splitext(filename)[0]
                in_file = extracted[base + '.in']
                ok_file = extracted[base + '.ok']

                new_testcase = Testcase(dataset_id=new_dataset.id,
                                        input_file=in_file,
                                        output_file=ok_file,
                                        codename=base)
                self.session.add(new_testcase)

    def create_empty_dataset(self, memory_limit, name, problem_id, time_limit):
        # Create a new dataset with no testcases
        new_dataset = Dataset(name=name,
                              problem_id=problem_id,
                              time_limit=time_limit,
                              memory_limit=memory_limit)
        self.session.add(new_dataset)
        self.session.flush() # Runs the insert, and sets the ID of the dataset
        return new_dataset

    def extract_zip(self, input_zip):

        zip_ref = zipfile.ZipFile(BytesIO(input_zip), 'r')

        return {name: zip_ref.read(name) for name in zip_ref.namelist()}

    def edit_dataset(self):
        pass
