# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>

from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from DB.Base import Base


class Problem_Contest(Base):
    __tablename__ = 'problems_contests'
    __table_args__ = (
        PrimaryKeyConstraint('problem_id', 'contest_id'),
        {}
    )

    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    contest_id = Column(Integer, ForeignKey("contests.id"), nullable=False)

    problem = relationship("Problem", back_populates="contests")
    contest = relationship("Contest", back_populates="problems")
