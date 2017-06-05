# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from DB import session_factory


class DBProcess(object):
    def acquire_sql_session(self):
        """
        Create an sql session and return it.
        :return: SQLAlchemy session object.
        """
        return session_factory()
