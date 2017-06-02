from DB.Entities import Testcase


class TestcaseRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Testcase).filter(Testcase.id == id)
        raise ValueError("id must be integer")
