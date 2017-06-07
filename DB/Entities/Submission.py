# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy import LargeBinary
from sqlalchemy import String

from DB.Entities import Base


class Submission(Base):
    """
    Object model for a submission
    A submission is sent to a problem with a specific participation id
    to specify the contest to with the submission has been sent
    """
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))  # TODO: index
    participation_id = Column(Integer,
                              ForeignKey("participations.id"),
                              nullable=True,
                              default=None)  # TODO: index
    file = Column(LargeBinary, nullable=False)
    executable_file = Column(LargeBinary, nullable=True, default=None)
    language = Column(String, nullable=False)

    created_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    in_compilation_queue = Column(Boolean, nullable=False, default=True)
    in_evaluation_queue = Column(Boolean, nullable=False, default=False)
