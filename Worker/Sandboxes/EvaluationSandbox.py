# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import os
import subprocess

from DB.Repositories import SubmissionRepository
from Worker.Checker import WhitespaceChecker
from Worker.Sandboxes.Sandbox import Sandbox
from Worker.Sandboxes.JobResult import JobResult, AbortJobResult


class EvaluationSandbox(Sandbox):
    def __init__(self, path, submission_id, worker_id):
        self.evaluation_path = os.path.join(path, 'sandbox_' +
                                            str(worker_id) +
                                            '_' +
                                            str(submission_id))
        super().__init__(self.evaluation_path)

    def parse_output(self, string):
        """
        Parse the output of the timeout format and split the results.
        :param string: Timeout command output
        :return: A tuple with the error code, message, cpu and memory
        """
        if not isinstance(string, str):
            string = string.decode('utf8')
        words = string.split(sep=' ')

        # Fail safe - linker error or others
        if len(words) < 7:
            return -4, string, 0, 0

        cpu, memory = 0, 0
        try:
            cpu = float(words[2])
            memory = float(words[6])
        except Exception:
            # Another fail safe - may be linker error or others
            return -4, string, 0, 0

        message = words[0]
        if message == "MEM":
            message = "MEMORY LIMIT EXCEEDED"
            code = -3
        elif message == "TIMEOUT":
            message = "TIME LIMIT EXCEEDED"
            code = -2
        else:
            message = ""
            code = 0

        return code, message, cpu, memory

    def evaluate(self,
                 submission_id,
                 stdin,
                 stdout,
                 executable_name,
                 in_testcase_path,
                 out_testcase_path,
                 time_limit=1.0,
                 memory_limit=64.0,
                 checker=WhitespaceChecker()):
        """
        Evaluate a given submission with given settings.

        This implementation is thread-safe.
        :param submission_id: Id of the submission being evaluated.
        :param stdin: The file from where the executable need to fetch data.
                      Empty or None for console stdin.
        :param stdout: The file to where the executable will send data.
                       Empty or None for console stdout.
        :param executable_name: The name of the executable to create.
        :param in_testcase_path: The actual path of the input test case.
        :param out_testcase_path: The actual path of the output test case.
        :param time_limit: The max time in seconds that the executable
                           is allowed to run.
        :param memory_limit: The max memory in mb the executable
                             is allowed to use.
        :param checker: The checker to use. Defaults to whitespace checker.
        :return: A JobResult object representing the status.
        """

        # Grab the submission first

        print("Evaluation submission with id " + str(submission_id))

        session = self.acquire_sql_session()
        submission = SubmissionRepository.get_by_id(session, submission_id)
        session.close()
        language = submission.language

        executable_path = self.get_by_relative_path(
            os.path.join(self.evaluation_path,
                         executable_name))

        # Create executable file
        self.create_executable(executable_path, submission.executable_file)

        # Create link to input
        testcase_link = os.path.join(self.evaluation_path,
                                     stdin if stdin is not None
                                     else str(submission_id) + '.in')
        try:
            self.remove_file(testcase_link)
        except:
            pass
        finally:
            self.create_link(testcase_link, in_testcase_path)

        # Create empty output
        testcase_output = os.path.join(self.evaluation_path,
                                       stdout if stdout is not None
                                       else str(submission_id) + '.out')
        try:
            self.remove_file(testcase_output)
        except:
            pass
        finally:
            self.create_writeonly(testcase_output)

        result = None
        if language in self.evaluation_strings:
            evaluation_command = self.evaluation_strings[language] \
                                 % executable_path

            if stdin is None or stdin == '':
                evaluation_command += ' < ' + testcase_link + ' '
            if stdout is None or stdout == '':
                evaluation_command += ' > ' + testcase_output + ' '

            # Actually execute the file
            message, cpu, memory = 0, 0, 0
            try:
                output = subprocess.check_output(['/usr/local/bin/timeout',
                                                  '-t',
                                                  str(time_limit),
                                                  '-m',
                                                  str(int(memory_limit *
                                                          1024.0)),
                                                  evaluation_command],
                                                 cwd=self.evaluation_path,
                                                 stderr=subprocess.STDOUT)
                print("Evaluation status: " + output.decode('utf8'))
                code, message, cpu, memory = self.parse_output(output)
                if code != 0:
                    result = JobResult(code,
                                       message,
                                       cpu=cpu,
                                       memory=memory)
            except subprocess.CalledProcessError as error:
                print("Evaluation error: " + error.output.decode('utf8'))
                code, message, cpu, memory = self.parse_output(error.output)
                result = JobResult(code,
                                   message,
                                   cpu=cpu,
                                   memory=memory)
            except Exception as err:
                print("Internal error: " + str(err))

                result = AbortJobResult()
            finally:
                self.remove_file(testcase_link)
                self.remove_file(executable_path)
            if result is None:
                is_valid = checker.check(in_testcase_path,
                                         out_testcase_path,
                                         testcase_output)
                if not is_valid:
                    return JobResult(-1,
                                     "WRONG ANSWER!",
                                     cpu=cpu,
                                     memory=memory)
                else:
                    return JobResult(0,
                                     "ACCEPTED!",
                                     cpu=cpu,
                                     memory=memory)
            else:
                return result
