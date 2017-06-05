# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

from DB.Entities import Dataset


class DatasetRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Dataset)\
                .filter(Dataset.id == id).one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_by_problem_id(session, id):
        if isinstance(id, int):
            return session.query(Dataset)\
                .filter(Dataset.problem_id == id).all()
        raise ValueError("id must be integer")
