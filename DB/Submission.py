# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, ForeignKey

from DB import Base


class Submission(Base):
    __tableName__ = 'submissions'
    id = Column(Integer, primary_key=True)
    problemId = Column(Integer, ForeignKey("problem.id"))  # TODO: index
    userId = Column(Integer, ForeignKey("user.id"))  # TODO: index
    result = Column(Integer)  # TODO: decide scoring and result types
