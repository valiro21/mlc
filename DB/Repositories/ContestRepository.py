# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import time

from DB.Entities import Contest


class ContestRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(Contest).filter(Contest.id == id)
        raise ValueError("id must be integer")

    @staticmethod
    def get_active_contests(session):
        current_time = time.time()
        return session.query(Contest)\
            .filter(Contest.start_time <= current_time)\
            .filter(current_time <= Contest.end_time +
                    Contest.length_of_contest)\
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
            .filter(Contest.start_time < current_time) \
            .order_by(Contest.start_time.desc())\
            .limit(limit)\
            .all()
