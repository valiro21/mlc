# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP

from DB.Entities import Base


class Log(Base):
    """
    Object model for all the changes made in
    the database
    """
    __tablename__ = 'logs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    process = Column(String)
    message = Column(String)
    level = Column(Integer)
    timestamp = Column(TIMESTAMP)
