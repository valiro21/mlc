# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from DB.Entities import Submission


class SubmissionRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Submission).filter(Submission.id == id).one()
        raise ValueError("id must be integer")
