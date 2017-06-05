# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import os
from threading import Lock

from DB.Repositories import TestcaseRepository
from Worker.Sandboxes.Sandbox import Sandbox


class TestcasesCacher(Sandbox):
    def __init__(self, path):
        super().__init__(os.path.join(path, 'testcases'))

        self.digests = {}
        self.locks = {}

    def prepare(self, dataset):
        """
        Cache all the testcases and keep the digest.
        We may need to update them if a change is detected.

        Only one process can actually execute the caching.
        :param dataset:
        :return:
        """
        # Initialize with database objects
        session = self.acquire_sql_session()
        testcases = TestcaseRepository.get_by_dataset_id(session, dataset.id)
        session.close()

        for testcase in testcases:
            self.refresh_testcase(testcase.id)

    def get_in_path(self, testcase_id):
        """
        Get path of the input file for a given testcase.
        :param testcase_id: Id of the testcases.
        :return: A string path
        """
        return os.path.join(self.base_path, str(testcase_id) + '.in')

    def get_out_path(self, testcase_id):
        """
        Get path of the output file for a given testcase.
        :param testcase_id: Id of the testcases.
        :return: A string path
        """
        return os.path.join(self.base_path, str(testcase_id) + '.ok')

    def acquire_lock(self, testcase_id):
        """
        Create a lock on testcase. Also acquire the lock.
        :param testcase_id: Id of the testcases.
        """
        if testcase_id not in self.locks:
            # Lock the object to ensure no duplicate locks are created
            self.lock.acquire()

            # Create the lock if we are the first worker to reach here
            if testcase_id not in self.locks:
                self.locks[testcase_id] = Lock()

            self.lock.release()

        self.locks[testcase_id].acquire()

    def release_lock(self, testcase_id):
        """
        Release lock on a testcase.
        :param testcase_id: Id of the testcases.
        """
        if testcase_id in self.locks:
            self.locks[testcase_id].release()

    def refresh_testcase(self, testcase_id):
        """
        Check the database for changes in testcase files and
        refresh the testcases if necesary.

        This is not thread safe. Use acquire_lock and release_lock
        for multiple threads to lock the testcase before caching.
        :param testcase_id: Id of the testcases.
        """
        session = self.acquire_sql_session()
        testcase = TestcaseRepository.get_by_id(session, testcase_id)
        session.close()

        # Assume the testcases don't need to be reloaded
        in_reload = False
        out_reload = False

        if testcase_id not in self.digests:
            # Reload all if digests are missing
            in_reload = True
            out_reload = True
        else:
            # Reload only if there are different digests
            in_digest, out_digest = self.digests[testcase_id]
            if in_digest != testcase.input_file_digest:
                in_reload = True
            if out_digest != testcase.output_file_digest:
                out_reload = True

        in_testcase_path = self.get_in_path(testcase.id)
        out_testcase_path = self.get_out_path(testcase.id)

        in_testcase = testcase.input_file
        out_testcase = testcase.output_file

        if in_reload:
            try:
                self.remove_file(in_testcase_path)
            except:
                # File does not exist
                pass
            finally:
                self.create_readonly(in_testcase_path, in_testcase)
        if out_reload:
            try:
                self.remove_file(out_testcase_path)
            except:
                # File does not exist
                pass
            finally:
                self.create_readonly(out_testcase_path, out_testcase)
