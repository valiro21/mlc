# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, String, Boolean, null

from DB import Base


class Contest(Base):
    __tableName__ = 'contests'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(Integer,
                  default=1,
                  nullable=False)  # 1 for open, 2 for public, 3 for private
    virtual = Column(Boolean, default=0, nullable=False)
    submission_download_allowed = Column(Boolean,
                                         default=True,
                                         nullable=False)
    allow_questions = Column(Boolean, default=True, nullable=False)
    allow_user_test = Column(Boolean, default=True, nullable=False)
    restricted_ip = Column(String, default='255.255.255.255', nullable=False)

    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    timezone = Column(String, dafault=null)
    length_of_contest = Column(Integer, dafault=null)
    max_submissions = Column(Integer, dafault=null)
    max_user_test = Column(Integer, default=null)
    min_submission_interval = Column(Integer, default=0, nullable=False)
    min_user_test_interval = Column(Integer, default=0, nullable=False)