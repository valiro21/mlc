# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
import os
import subprocess

from Worker.Sandboxes.JobResult import ValidJobResult, JobResult
from Worker.Sandboxes.Sandbox import Sandbox


class CompilationSandbox(Sandbox):
    """
    Sandbox for compilation purposes.
    """

    def __init__(self, path, submission_id):
        super().__init__(os.path.join(path, 'compile_' + str(submission_id)))

    def remove_timeout_str(self, string):
        """
        Remove output from timeout command. This is used to
        show only the relevant errors.
        :param string: Output to clean.
        :return: Clean string.
        """
        if not isinstance(string, str):
            string = string.decode('utf8')

        lines = string.split(sep='\n')
        # Can be either the last line or the one before
        # I don't really know why :))
        if len(lines) >= 1 and "FINISHED" in lines[-1]:
            del lines[-1]

        if len(lines) >= 2 and "FINISHED" in lines[-2]:
            del lines[-2]

        return "\n".join(lines)

    def compile(self,
                submission,
                problem,
                time_limit=3.0):
        """
        Compile the submission for a given problem.
        :param submission: The submission to compile.
        :param problem: The problem the submission was sent to.
        :param time_limit: Maximum compilation time.
        :return: A JobResult object with the compilation results.
        """

        # Logs
        print("Compiling submission with id " + str(submission.id))

        # Get actual file extension for language.
        # If there is no extension available, then the language is invalid.

        ext = self.get_lang_ext(submission.language)
        if ext is None:
            print("Invalid language for submission with id " +
                  str(submission.id))
            return JobResult(1, "Invalid of unsupported language!")

        executable_path = self.get_by_relative_path(problem.name)

        language = submission.language
        if language in self.compilation_strings:
            # Create source file
            self.create_source_file(problem.name + '.' + ext, submission.file)

            compilation_settings = self.compilation_strings[language]

            # For languages where compilation is not necessary
            # just check the syntax
            if compilation_settings['output']:
                compilation_command = compilation_settings['string'] \
                                      % (executable_path, problem.name)
            else:
                compilation_command = compilation_settings['string'] \
                                      % (problem.name)

            # Actually compile the file
            results = ValidJobResult("Compilation OK.")
            try:
                output = subprocess.check_output(['/usr/local/bin/timeout',
                                                  '-t',
                                                  str(time_limit),
                                                  compilation_command],
                                                 stderr=subprocess.STDOUT,
                                                 cwd=self.base_path)
                print(output)

                if not compilation_settings['output']:
                    executable_path = self.get_by_relative_path(problem.name +
                                                                '.' +
                                                                ext)
                with open(executable_path, 'rb') as file:
                    s = file.read()
                    submission.executable_file = s
                    print("Compilation succeeded!")
            except subprocess.CalledProcessError as error:
                decoded_error = self.remove_timeout_str(
                    error.output.decode('utf8')
                )
                print("Compilation failed with error: " + decoded_error)
                results = JobResult(error.returncode, decoded_error)
            except Exception as err:
                print("Compilation failed with error: " + str(err))
                results = JobResult(err.args[0][0], err.args[0][1])
            finally:
                self.remove_file(problem.name)
                return results

        print("Invalid extension " +
              language +
              " for submission with id " +
              str(submission.id))
        return JobResult(1, "Invalid extension " + language)
