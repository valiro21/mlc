# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, ForeignKey, null
from sqlalchemy import LargeBinary
from sqlalchemy import String

from DB.Entities import Base


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))  # TODO: index
    participation_id = Column(Integer,
                              ForeignKey("participations.id"))  # TODO: index
    file = Column(LargeBinary, nullable=False)
    executable_file = Column(LargeBinary, nullable=True, default=null)
    language = Column(String, nullable=False)
    compilation_code = Column(Integer, default=null)
    compilation_message = Column(String, default=null)
    evaluation_code = Column(Integer, default=null)
    evaluation_message = Column(String, default=null)
