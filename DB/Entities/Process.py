# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP

from DB.Entities import Base


class Process(Base):
    """
    Object model for a submission
    """
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_report_time = Column(TIMESTAMP)
    status = Column(Integer)
