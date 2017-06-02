from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP

from DB.Entities import Base


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    process = Column(String)
    message = Column(String)
    level = Column(Integer)
    timestamp = Column(TIMESTAMP)
