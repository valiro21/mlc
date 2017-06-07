# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
import subprocess

from Worker.Checker import Checker


class WhitespaceChecker(Checker):
    @staticmethod
    def is_whitespace(c):
        return c in ['\n', '\t', ' ']

    def check(self,
              in_testcase,
              out_testcase,
              out_contestant):

        try:
            subprocess.check_output(['diff',
                                     '-b',  # Ignore whitespace
                                     out_testcase,
                                     out_contestant])
        except subprocess.CalledProcessError:
            return False
        finally:
            return True
