# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
import time
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, Boolean

from DB.Entities import Base
from DB.Utils import nvl


class Contest(Base):
    __tablename__ = 'contests'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    problems = relationship("Problem_Contest", back_populates="contest")

    type = Column(Integer,
                  default=1,
                  nullable=False)  # 1 for open, 2 for public, 3 for private
    virtual = Column(Boolean, default=True, nullable=False)
    submission_download_allowed = Column(Boolean,
                                         default=True,
                                         nullable=False)
    allow_questions = Column(Boolean, default=True, nullable=False)
    allow_user_test = Column(Boolean, default=True, nullable=False)
    restricted_ip = Column(String, default='255.255.255.255', nullable=False)

    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    timezone = Column(String, default='UTC+0')
    length_of_contest = Column(Integer, default=0, nullable=False)
    max_submissions = Column(Integer, default=100, nullable=False)
    max_user_test = Column(Integer, default=100, nullable=False)
    min_submission_interval = Column(Integer, default=0, nullable=False)
    min_user_test_interval = Column(Integer, default=0, nullable=False)

    @staticmethod
    def get_active_contests(session):
        current_time = int(time.time())
        contests = session.query(Contest) \
            .filter(Contest.start_time <= current_time)\
            .filter(current_time <=
                    Contest.end_time + nvl(Contest.end_time, 0))
        return contests
