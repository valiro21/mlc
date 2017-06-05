# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from DB.Entities import Testcase


class TestcaseRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Testcase)\
                .filter(Testcase.id == id)\
                .one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_by_dataset_id(session, id):
        if isinstance(id, int):
            return session.query(Testcase)\
                .filter(Testcase.dataset_id == id)\
                .all()
        raise ValueError("id must be integer")
