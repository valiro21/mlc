# Copyright ? 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright ? 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright ? 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright ? 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from DB.Entities.ContestPermissions import ContestPermissions


class ContestPermissionsRepository:
    @staticmethod
    def check_permission(session, contest_id, user_id):
        """
        Return True if a user had permission to modify
        the contest with contest_id
        :param session:
        :param contest_id:
        :param user_id:
        :return: Boolean
        """
        check = session.query(ContestPermissions). \
            filter(ContestPermissions.user_id == user_id). \
            filter(ContestPermissions.contest_id == contest_id).one()
        if check is None:
            return False
        return True
