# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

from Worker.Checker import Checker


class WhitespaceChecker(Checker):
    @staticmethod
    def is_whitespace(c):
        return c in ['\n', '\t', ' ']

    def check(self,
              in_testcase,
              out_testcase,
              out_contestant):

        with open(out_testcase) as fo, open(out_contestant) as fc:
            while True:
                c1 = fo.read(1)
                whitespace_c1 = False
                while c1 and WhitespaceChecker.is_whitespace(c1):
                    whitespace_c1 = True
                    c1 = fo.read(1)

                c2 = fc.read(1)
                whitespace_c2 = False
                while c2 and WhitespaceChecker.is_whitespace(c2):
                    whitespace_c2 = True
                    c2 = fc.read(1)

                if not c1 and not c2:
                    break
                elif not c1 or not c2:
                    return False
                elif whitespace_c1 != whitespace_c2:
                    return False
                elif c1 != c2:
                    return False
        return True
