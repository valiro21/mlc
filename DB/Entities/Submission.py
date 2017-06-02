# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import LargeBinary
from sqlalchemy import String

from DB.Entities import Base


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    problemId = Column(Integer, ForeignKey("problems.id"))  # TODO: index
    userId = Column(Integer, ForeignKey("users.id"))  # TODO: index
    result = Column(Integer)  # TODO: decide scoring and result types
    file = Column(LargeBinary, nullable=False)
    file_digest = Column(String, nullable=False)
    executable_file = Column(LargeBinary, nullable=False)
