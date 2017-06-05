# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from Worker.Checker import Checker


class WhitespaceChecker(Checker):
    def is_whitespace(self, c):
        return c in ['\n', '\t', ' ']

    def are_equivalent(self, c1, c2):
        if self.is_whitespace(c1) and self.is_whitespace(c2):
            return True
        else:
            return c1 == c2

    def check(self,
              in_testcase,
              out_testcase,
              out_contestant):

        with open(out_testcase) as fo, open(out_contestant) as fc:
            while True:
                c1 = fo.read(1)
                c2 = fc.read(1)

                if not c1 and not c2:
                    break
                elif not c1 or not c2:
                    return False
                elif not self.are_equivalent(c1, c2):
                    return False
        return True
