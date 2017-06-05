# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import os

from DB.Repositories import DatasetRepository
from Worker.Sandboxes.DatasetSandbox import DatasetSandbox
from Worker.Sandboxes.Sandbox import Sandbox


class ProblemSandbox(Sandbox):
    """
    Sandbox holding caches for datasets of a problem.
    """

    def __init__(self, path, problem):
        super().__init__((os.path.join(path, str(problem.id))))
        self.problem_name = problem.name

        self.datasets_sandboxes = {}

    def prepare(self, problem):
        """
        Cache the entire problem. Not thread-safe.
        Only one process can actually execute the caching.
        :param problem: SQLAlchemy object representing the problem
        """
        session = self.acquire_sql_session()
        datasets = DatasetRepository \
            .get_by_problem_id(session, problem.id)
        session.close()

        # Initialize sandboxes for Datasets

        for dataset in datasets:
            if dataset.id not in self.datasets_sandboxes:
                sandbox = DatasetSandbox(self.base_path,
                                         problem.name,
                                         dataset)
                sandbox.prepare(dataset)
                self.datasets_sandboxes[dataset.id] = sandbox

    def evaluate(self, dataset_id, testcase_id, submission_id, worker_id):
        """
        Evaluate submission with the given id on testcase with the given id.

        The worker id is needed for unique sandbox folder creation.
        The dataset_id is needed for dataset sandbox loading.

        This implementation is thread-safe.
        :param dataset_id: Id of the dataset being evaluated.
        :param testcase_id: Id of the testcase being evaluated.
        :param submission_id: Id of the submission being evaluated.
        :param worker_id: Id of the worked that does the evaluation.
        :return: A JobResults object with the evaluation status.
        """
        if dataset_id not in self.datasets_sandboxes:
            # Lock the entire object to add the dataset

            self.lock.acquire()

            # Recheck for any changes made by other threads
            if dataset_id not in self.datasets_sandboxes:
                session = self.acquire_sql_session()
                dataset = DatasetRepository.get_by_id(session, dataset_id)
                session.close()

                # Create subtree for the problem
                sandbox = DatasetSandbox(self.base_path,
                                         self.problem_name,
                                         dataset)
                self.datasets_sandboxes[dataset_id] = sandbox
            self.lock.release()

        sandbox = self.datasets_sandboxes[dataset_id]
        return sandbox.evaluate(testcase_id, submission_id, worker_id)
