# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>


class JobResult:
    def __init__(self, code, message, cpu=0, memory=0):
        self.code = code
        self.message = message
        self.cpu = cpu
        self.memory = memory

    def is_valid(self):
        return True if self.code == 0 else False


class ValidJobResult(JobResult):
    def __init__(self, message, cpu=0, memory=0):
        super().__init__(0, message, cpu=cpu, memory=memory)


class AbortJobResult(JobResult):
    def __init__(self,
                 code=-1000,
                 message="Internal error",
                 cpu=-1,
                 memory=-1):
        super().__init__(code, message, cpu, memory=memory)
