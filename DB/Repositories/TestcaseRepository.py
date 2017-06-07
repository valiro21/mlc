# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from DB.Entities import Testcase


class TestcaseRepository:
    @staticmethod
    def get_by_id(session, id):
        """
        Gets a testcase by it's id
        :param session:
        :param id:
        :return: a testcase
        """
        if isinstance(id, int):
            return session.query(Testcase)\
                .filter(Testcase.id == id) \
                .filter(Testcase.deleted.is_(False))\
                .one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_by_dataset_id(session, id):
        """
        Gets all the testcases of a dataset
        :param session:
        :param id:
        :return: a list of testcases
        """
        if isinstance(id, int):
            return session.query(Testcase)\
                .filter(Testcase.dataset_id == id)\
                .filter(Testcase.deleted.is_(False))\
                .all()
        raise ValueError("id must be integer")

    @staticmethod
    def delete_by_id(session, id):
        """
        Deletes a testcase by it's id
        :param session:
        :param id:
        """
        if isinstance(id, int):
            session.query(Testcase)\
                .filter_by(id=id)\
                .update({'deleted': True})
        else:
            raise ValueError("id must be integer")
