# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

import time

from pyparsing import basestring
from sqlalchemy.exc import SQLAlchemyError

from DB.Entities import Contest, Problem_Contest, Problem


class ContestRepository:
    @staticmethod
    def get_by_name(session, name):
        if isinstance(name, basestring):
            return session.query(Contest).filter(Contest.name == name).one()
        raise ValueError("name must be string")

    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Contest).filter(Contest.id == id).one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_active_contests(session):
        current_time = time.time()
        return session.query(Contest)\
            .filter(Contest.start_time <= current_time)\
            .filter(current_time <= Contest.end_time +
                    Contest.length_of_contest)\
            .filter(Contest.id != 1)\
            .all()

    @staticmethod
    def get_future_contests(session):
        current_time = time.time()
        return session.query(Contest) \
            .filter(current_time < Contest.start_time)\
            .all()

    @staticmethod
    def get_recent_contests(session, limit=10):
        current_time = time.time()
        return session.query(Contest) \
            .filter(Contest.end_time +
                    Contest.length_of_contest < current_time) \
            .order_by(Contest.start_time.desc())\
            .limit(limit)\
            .all()

    @staticmethod
    def get_all_contest_order_by_date(session):
        return session.query(Contest) \
            .order_by(Contest.start_time.desc()) \
            .all()

    @staticmethod
    def has_problem(session, contest_id, problem_id):
        """Returns true if problem specified by problem_id
        belongs to contest specified by contest_id"""

        try:
            session.query(Problem_Contest)\
                .filter_by(problem_id=problem_id)\
                .filter_by(contest_id=contest_id).one()
        except SQLAlchemyError:
            return False
        return True

    @staticmethod
    def get_all_problems(session, contest_id):
        """Returns a list of all problems belonging to the
        contest specified by the contest_id"""

        return session.query(Problem)\
            .join(Problem_Contest, Problem_Contest.problem_id == Problem.id)\
            .join(Contest, Contest.id == Problem_Contest.contest_id)\
            .filter(Contest.id == contest_id)\
            .all()

    @staticmethod
    def add_problem(session, contest, problem):
        """Adds given problem to contest"""
        new_relation = Problem_Contest(problem_id=problem.id,
                                       contest_id=contest.id)
        session.add(new_relation)
        session.commit()

    @staticmethod
    def remove_problem(session, contest, problem):
        """Removes problem from given contest"""

        relation = session\
            .query(Problem_Contest)\
            .filter(Problem_Contest.problem_id == problem.id)\
            .filter(Problem_Contest.contest_id == contest.id)\
            .one()
        session.delete(relation)
        session.commit()
