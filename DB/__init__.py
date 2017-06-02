# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DB import Contest, Participation, \
    Problem, User, Submission, Dataset, \
    Testcase, Permission, Admin, Admin_Permission
from DB import Base


def nvl(value, empty):
    return empty if value == '' else value

with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') \
        as config_file:

    config = json.load(config_file)

    connection_string = config['custom_connection_string']
    if connection_string is '':
        db_driver = config['database_driver']
        db_user = config['database_user']
        db_password = config['database_password']
        db_name = nvl(config['database_name'], 'database')
        db_host = nvl(config['database_host'], 'localhost')
        db_port = nvl(config['database_port'], '5432')
        connection_string = db_driver + "://" + db_user + \
            (":" + db_password
             if db_password is not ''
             else '') + \
            "@" + db_host + ":" + db_port + "/" + db_name

    engine = create_engine(connection_string)

    session_factory = sessionmaker()
    session_factory.configure(bind=engine)

    Base.Base.metadata.create_all(engine)

__all__ = [
    "Contest", "Problem", "Submission",
    "User", "Dataset", "Testcase",
    "Participation", "Admin", "Permission", "Admin_Permission",
    "session_factory"
]
