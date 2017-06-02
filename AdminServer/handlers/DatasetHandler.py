"""Dataset Handler for AdminWebServer."""

# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

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

        functions = {'create': getattr(self, 'create_dataset'),
                     'edit': getattr(self, 'edit_dataset')}

        path_elements = [x for x in self.request.path.split("/") if x]
        action = path_elements[-1]

        if action in functions.keys():
            functions[action]()
        else:
            raise HTTPError(404)

    def create_dataset(self):

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
            raise HTTPError(400) # Bad request

        # Create a new dataset with no testcases
        new_dataset = None
        try:
            new_dataset = Dataset(name=name,
                                  problem_id=problem_id,
                                  time_limit=time_limit,
                                  memory_limit=memory_limit)
            self.session.add(new_dataset)
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            self.redirect('/error/from/datasethandler')
            return

        # TODO: test if zip, extract zip, get legit testcases etc

        # Create the new testcases
        try:
            new_testcase = Testcase(dataset_id=new_dataset.id,
                                    input_file=testcases_body,
                                    input_file_digest=b'as',
                                    output_file=b'output',
                                    output_file_digest=b'werf')
            self.session.add(new_testcase)
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            self.redirect('/error/datasethandler')
            return

        # TODO: test if testcases are added successfully,
        # TODO: else, delete the dataset

        print(new_dataset)
        print(new_testcase)

        # self.redirect('/problem/' + new_dataset.problem.name)

    def edit_dataset(self):
        pass
