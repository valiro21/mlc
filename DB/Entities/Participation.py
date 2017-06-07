# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from DB.Entities import Base


class Participation(Base):
    """
    Object model for the contests participation
    if a user is registered to a contest it must
    have a participation for that contest
    """
    __tablename__ = 'participations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contest_id = Column(Integer, ForeignKey("contests.id"))
    type = Column(Integer,
                  default=1,
                  nullable=False)  # 1 is official, 2 is unofficial
    unrestricted = Column(Boolean,
                          default=False,
                          nullable=False)
    hidden = Column(Boolean, default=False, nullable=False)
    delay_time = Column(Integer, default=0, nullable=False)
    extra_time = Column(Integer, default=0, nullable=False)
    special_password = Column(String, default=None)
