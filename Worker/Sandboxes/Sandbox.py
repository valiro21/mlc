# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>

import os
import shutil
from threading import Lock

from Worker.DBProcess import DBProcess


class Sandbox(DBProcess):
    """
    Class that creates a sandbox environment. This class represents
    an actual filesystem and has it's own methods for creating secure
    files and folders.

    It is guaranteed a secure environment for the execution and compilation.
    """

    compilation_strings = {
        'C': {
            'string': 'gcc -std=c11 -O2 -pipe -DONLINE_JUDGE -s -o '
                      '%s %s.c',
            'output': True
        },
        'C++': {
            'string': 'g++ -std=c++11 -O2 -pipe -DONLINE_JUDGE -s -o '
                      '%s %s.cpp',
            'output': True
        },
        'Haskell': {
            'string': 'ghc -static -O2 -Wall -o %s %s.hs',
            'output': True
        },
        'Python': {
            'string': 'python -m py_compile %s.py',
            'output': False
        }
    }

    evaluation_strings = {
        'C': '%s',
        'C++': '%s',
        'Python': 'python3 %s.py',
        'Haskell': '%s'
    }

    language_extensions = {
        'C': 'c',
        'C++': 'cpp',
        'Python': 'py',
        'Haskell': 'hs',
        'Javascript': 'js'
    }

    def get_lang_ext(self, lang):
        """
        Get extension used by a specific programming language
        :return: String representing the extension
        """
        if lang not in self.language_extensions:
            return None
        return self.language_extensions[lang]

    def create_source_file(self, path, data):
        """
            Create a file for compilation
            :param path: relative path to the sandbox location
            :param data: data to fill the file with
        """
        absolute_path = self.get_by_relative_path(path)
        file = os.open(absolute_path, os.O_CREAT | os.O_WRONLY)
        if data is not None:
            os.write(file, data)
        os.close(file)

    def create_executable(self, path, data):
        """
        Create a file with executable permissions.
        :param path: relative path to the sandbox location
        :param data: data to fill the executable with
        """
        absolute_path = self.get_by_relative_path(path)
        file = os.open(absolute_path, os.O_CREAT | os.O_WRONLY)
        if data is not None:
            os.write(file, data)
        os.close(file)

    def create_readonly(self, path, data):
        """
        Create a file with readonly permissions.
        :param path: relative path to the sandbox location
        :param data: data to fill the file with
        """
        absolute_path = self.get_by_relative_path(path)
        file = os.open(absolute_path, os.O_CREAT | os.O_WRONLY)
        if data is not None:
            os.write(file, data)
        os.close(file)
        os.chmod(absolute_path, 0o774)

    def create_writeonly(self, path):
        """
        Create a file with writeonly permissions.
        :param path: relative path to the sandbox location
        :param data: data to fill the file with
        """
        absolute_path = self.get_by_relative_path(path)
        file = os.open(absolute_path, os.O_CREAT | os.O_WRONLY)
        os.close(file)
        os.chmod(absolute_path, 0o772)

    def create_link(self, link_path, actual_file_path):
        """
        Create a symbolic link to a file.
        :param link_path: link relative path to the sandbox location
        :param actual_file_path: file relative path to the sandbox location
        """
        absolute_link_path = self.get_by_relative_path(link_path)
        file_path = self.get_by_relative_path(actual_file_path)
        os.symlink(file_path, absolute_link_path)

    def unlink(self, path):
        """
        Remove a link from sandbox.
        :param path: relative path the the sandbox
        :return: True if the operation succeeded, False otherwise
        """
        absolute_path = self.get_by_relative_path(path)
        try:
            os.unlink(absolute_path)
            return True
        except:
            return False

    def remove_file(self, path):
        """
        Remove a file from sandbox.
        :param path: relative path the the sandbox
        :return: True if the operation succeeded, False otherwise
        """
        absolute_path = self.get_by_relative_path(path)
        try:
            os.remove(absolute_path)
            return True
        except:
            return False

    def get_by_relative_path(self, *args):
        """
        Given a list of string, return the absolute path
        relative to this sandbox of the path constructed
        by string concatenation. The strings will be joined
        with '/'.
        :param args: Path strings to join
        :return: An absolute path
        """
        path = self.base_path
        for arg in args:
            if isinstance(arg, str):
                path = os.path.join(path, arg)
        return path

    def __init__(self, path='/tmp/sandbox'):
        super().__init__()
        self.base_path = os.path.abspath(path)
        self.lock = Lock()
        try:
            os.mkdir(self.base_path)
        except Exception:
            pass
        os.chmod(self.base_path, 0o771)

    def __del__(self):
        shutil.rmtree(self.base_path)
