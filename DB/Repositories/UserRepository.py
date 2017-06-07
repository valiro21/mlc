# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from pyparsing import basestring

from DB.Entities import User


class UserRepository:
    @staticmethod
    def get_by_id(session, id):
        """
        Gets a user by its id
        :param session:
        :param id:
        :return: a User entity
        """
        if isinstance(id, int):
            return session.query(User).filter(User.id == id).one()
        raise ValueError("id must be integer")

    @staticmethod
    def get_most_rated(session, limit=10):
        """
        Gets a list of users ordered by their rating
        :param session:
        :param limit:
        :return: a list of Users
        """
        return session.query(User)\
            .order_by(User.rating.desc())\
            .limit(limit)

    @staticmethod
    def get_by_name(session, name):
        """
        Gets a user by its name
        :param session:
        :param name:
        :return: a User entity
        """
        if isinstance(name, basestring):
            return session.query(User).filter(User.username == name).one()
        raise ValueError("name must be string")
