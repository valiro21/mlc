# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

from DB.Entities import Base


class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    problem_id = Column(Integer,
                        ForeignKey("problems.id", ondelete='SET NULL'))
    problem = relationship('Problem',
                           backref=backref('datasets',
                                           cascade='all, delete-orphan'),
                           foreign_keys=problem_id)

    testcases = relationship('Testcase',
                             backref='dataset',
                             cascade='all, delete-orphan')

    stdin = Column(String, nullable=False)  # empty string is stdin
    stdout = Column(String, nullable=False)  # empty string is stdout

    time_limit = Column(Float, default=1, nullable=False)
    memory_limit = Column(Float, default=16, nullable=False)
