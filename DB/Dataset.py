# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from sqlalchemy import Column, Integer, String, null, ForeignKey, Float

from DB import Base


class Dataset(Base):
    __tableName__ = 'dataset'
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("Problem.id"))
    name = Column(String)
    input_file = Column(String, default=null)
    output_file = Column(String, default=null)
    time_limit = Column(Float, default=1, nullable=False)
    memory_limit = Column(Float, default=16, nullable=False)
