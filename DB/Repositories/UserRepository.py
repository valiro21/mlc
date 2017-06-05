# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from pyparsing import basestring

from DB.Entities import User


class UserRepository:
    @staticmethod
    def get_by_id(session, id):
        if isinstance(id, int):
            return session.query(User).filter(User.id == id)
        raise ValueError("id must be integer")

    @staticmethod
    def get_most_rated(session, limit=10):
        return session.query(User)\
            .order_by(User.rating.desc())\
            .limit(limit)

    @staticmethod
    def get_by_name(session, name):
        if isinstance(name, basestring):
            return session.query(User).filter(User.username == name).first()
        raise ValueError("name must be string")
