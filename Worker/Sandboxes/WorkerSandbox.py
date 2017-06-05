# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from DB.Repositories import ProblemRepository, SubmissionRepository
from Worker.Sandboxes.ProblemSandbox import ProblemSandbox
from Worker.Sandboxes.CompilationSandbox import CompilationSandbox
from Worker.Sandboxes.Sandbox import Sandbox


class WorkerSandbox(Sandbox):
    def prepare(self):
        self.lock.acquire()
        session = self.acquire_sql_session()
        problems = ProblemRepository.get_problems_of_active_contests(session)
        session.close()

        self.problems_sandboxes = {}
        for problem in problems:
            sandbox = ProblemSandbox(self.base_path, problem)
            self.problems_sandboxes[str(problem.id)] = sandbox
        self.lock.release()

    def compile(self, submission_id):
        session = self.acquire_sql_session()
        submission = SubmissionRepository.get_by_id(session, submission_id)
        problem = ProblemRepository.get_by_id(session, submission.problem_id)

        sandbox = CompilationSandbox(self.base_path, submission_id)
        result = sandbox.compile(submission, problem)
        del sandbox
        session.commit()
        session.close()

        return submission_id, \
            -1, \
            -1, \
            result

    def evaluate(self,
                 problem_id,
                 dataset_id,
                 testcase_id,
                 submission_id,
                 worker_id):
        if problem_id not in self.problems_sandboxes:
            # Lock the entire object to add the dataset

            self.lock.acquire()

            # Recheck for any changes made by other threads
            if dataset_id not in self.problems_sandboxes:
                session = self.acquire_sql_session()
                problem = ProblemRepository.get_by_id(session, problem_id)
                session.close()

                # Create subtree for the problem
                sandbox = ProblemSandbox(self.base_path, problem)
                self.problems_sandboxes[dataset_id] = sandbox
            self.lock.release()

        sandbox = self.problems_sandboxes[dataset_id]

        return submission_id, \
            dataset_id, \
            testcase_id, \
            sandbox.evaluate(dataset_id,
                             testcase_id,
                             submission_id,
                             worker_id)
