# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

import time

from DB.Entities import Problem, Contest, Problem_Contest


class ProblemRepository:
    @staticmethod
    def get_by_id(session, id):
        """
        Gets a problem by id
        :param session:
        :param id:
        :return: a problem entity
        """
        if isinstance(id, int):
            return session.query(Problem).filter(Problem.id == id).one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_problems_of_active_contests(session):
        """
        Gets a list of problems that are active in the current
        contests
        :param session:
        :return:a list of problems
        """
        current_time = time.time()
        return session.query(Problem) \
            .join(Problem_Contest,
                  Problem.id == Problem_Contest.contest_id) \
            .join(Contest,
                  Problem_Contest.problem_id == Contest.id) \
            .filter(Contest.start_time <= current_time) \
            .filter(current_time <= Contest.end_time +
                    Contest.length_of_contest) \
            .distinct() \
            .all()

    @staticmethod
    def get_by_name(session, name):
        """
        Gets a problem by it's name
        :param session:
        :param name:
        :return: a problem entity
        """
        if isinstance(name, str):
            return session.query(Problem).filter_by(name=name) \
                .one()
        raise ValueError("name must be string")

    @staticmethod
    def update_default_dataset(session, problem_id):
        """ If the problem has no active dataset,
        it tries to assign it one."""

        if isinstance(problem_id, int):
            problem = session.query(Problem) \
                .filter_by(id=problem_id).one()
            if problem.active_dataset_id is None and \
                    len(problem.datasets) > 0:

                # Select the first dataset as the default
                problem.active_dataset_id = problem.datasets[0].id
        else:
            raise ValueError("id must be integer")
