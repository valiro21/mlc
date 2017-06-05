# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from Worker.WorkerProcess import WorkerProcess
from tornado.ioloop import IOLoop

if __name__ == '__main__':
    ioloop = IOLoop.instance()
    process = WorkerProcess(ioloop, 'mlcdb')

    ioloop.start()
