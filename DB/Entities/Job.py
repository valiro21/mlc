# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP

from DB.Entities import Base


class Job(Base):
    """
    Class used to describe a job for a worker.
    For example we need to evaluate testcase 4 on problem 2
    in contest 1. This table is used for queueing tasks.
    """
    __tablename__ = 'jobs'

    submission_id = Column(Integer, nullable=False, primary_key=True)
    submission_id.__doc__ = 'ID of the submission'

    contest_id = Column(Integer, nullable=True)
    contest_id.__doc__ = 'The type of the contest.'

    job_type = Column(String)
    job_type.__doc__ = 'The type of the task.'

    status_message = Column(String, nullable=True)
    status_message.__doc__ = 'Compilation of evaluation message.'

    time_limit = Column(Float, nullable=False, default=1)
    time_limit.__doc__ = 'Time limit in seconds.'

    memory_limit = Column(Float, nullable=False, default=64)
    memory_limit.__doc__ = 'Memory limit in MB'

    timestamp = Column(TIMESTAMP, nullable=False)
    timestamp.__doc__ = 'The timestamp when the task was created.'

    estimated_finish_timestamp = Column(TIMESTAMP, nullable=True)
    estimated_finish_timestamp.__doc__ = 'The expected timestamp when ' \
                                         'the job should be finished.'

    worker_id = Column(Integer, nullable=True)
    worker_id.__doc__ = 'The id of the worker that executes the job.'

    status = Column(Integer, nullable=False, default=1)
    status.__doc__ = 'Status of the job.'

    score = Column(Integer, nullable=False)
    score.__doc__ = 'Score given by a scoring heuristic to determine ' \
                    'the execution priority.'
