# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import time

from sqlalchemy.orm.exc import NoResultFound


from DB.Entities import Problem, Contest, Problem_Contest


class ProblemRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Problem).filter(Problem.id == id).one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_problems_of_active_contests(session):
        current_time = time.time()
        return session.query(Problem)\
            .join(Problem_Contest,
                  Problem.id == Problem_Contest.contest_id) \
            .join(Contest,
                  Problem_Contest.problem_id == Contest.id)\
            .filter(Contest.start_time <= current_time)\
            .filter(current_time <= Contest.end_time +
                    Contest.length_of_contest)\
            .distinct()\
            .all()

    @staticmethod
    def get_by_name(session, name):
        if isinstance(name, str):
            try:
                return session.query(Problem).filter_by(name=name)\
                    .one()
            except NoResultFound as err:
                return None
        raise ValueError("name must be string")
