# Copyright ? 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright ? 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright ? 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

from sqlalchemy import Column, Integer, ForeignKey

from DB.Entities import Base


class ContestPermissions(Base):
    """
    Object model for the permission to modify contest
    an entry here means that the user with the specific id
    has permission to modify a contest with the specific id
    """
    __tablename__ = 'contest_permissions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contest_id = Column(Integer, ForeignKey("contests.id"))
