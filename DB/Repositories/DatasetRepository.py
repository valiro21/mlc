from DB.Entities import Dataset


class DatasetRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Dataset).filter(Dataset.id == id)
        raise ValueError("id must be integer")
