# Copyright ? 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright ? 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from DB import Participation


class ParticipationRepository:
    @staticmethod
    def verif_participation(session, user_id, contest_id):
        """
        Return True if the user with user_id is already
        a participant in the contests with contest_id
        :param session:
        :param user_id:
        :param contest_id:
        :return: Boolean
        """
        ok = session.query(Participation). \
            filter(Participation.user_id == user_id). \
            filter(Participation.contest_id == contest_id).first()
        if ok is None:
            return False
        return True
