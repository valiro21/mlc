# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from DB.Entities import Problem


class ProblemRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Problem).filter(Problem.id == id)
        raise ValueError("id must be integer")

    @staticmethod
    def get_problems_of_active_contests(session):
        pass
