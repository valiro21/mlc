from DB.Entities import Contest


class ContestRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Contest).filter(Contest.id == id)
        raise ValueError("id must be integer")
