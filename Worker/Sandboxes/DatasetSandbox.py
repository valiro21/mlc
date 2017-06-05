# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import os

from DB.Entities import Dataset
from DB.Repositories import DatasetRepository
from Worker.Sandboxes.Sandbox import Sandbox
from Worker.Sandboxes.EvaluationSandbox import EvaluationSandbox
from Worker.Sandboxes.TestcasesCacher import TestcasesCacher


class DatasetSandbox(Sandbox):
    """
    Sandbox holding caches for dataset testcases.
    """

    def __init__(self, path: str, problem_name: str, dataset: Dataset):
        super().__init__(os.path.join(path, str(dataset.id)))
        self.dataset_id = dataset.id
        self.problem_name = problem_name
        self.cacher = TestcasesCacher(self.base_path)

    def prepare(self, dataset: Dataset):
        """
        Cache a dataset completely. Not thread-safe.
        Only one process can actually execute the caching.
        :param dataset: Dataset to cache
        :return:
        """
        self.lock.acquire()
        self.cacher.prepare(dataset)
        self.lock.release()

        self.cacher.prepare(dataset)

    def evaluate(self, testcase_id: int, submission_id: int, worker_id: int):
        """
        Evaluate submission with the given id on testcase with the given id.
        The worker id is needed for unique sandbox folder creation.

        This implementation is thread-safe.
        :param testcase_id: Id of the testcase being evaluated.
        :param submission_id: Id of the submission being evaluated.
        :param worker_id: Id of the worked that does the evaluation.
        :return: A JobResults object with the evaluation status.
        """
        # Lock the entire testcase to add the dataset
        self.cacher.acquire_lock(testcase_id)

        self.cacher.refresh_testcase(testcase_id)

        self.cacher.release_lock(testcase_id)

        session = self.acquire_sql_session()
        dataset = DatasetRepository.get_by_id(session, self.dataset_id)
        session.close()

        evaluation_sandbox = EvaluationSandbox(
            self.base_path,
            submission_id,
            worker_id
        )
        result = evaluation_sandbox.evaluate(
            submission_id,
            dataset.stdin,
            dataset.stdout,
            self.problem_name,
            self.cacher.get_in_path(testcase_id),
            self.cacher.get_out_path(testcase_id),
            dataset.time_limit,
            dataset.memory_limit)
        del evaluation_sandbox
        return result
