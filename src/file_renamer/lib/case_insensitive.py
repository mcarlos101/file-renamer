import os
import logging
from pathlib import Path
from abc import ABC, abstractmethod


class CaseSensitive(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class CaseInsensitive(CaseSensitive):
    def __init__(self):
        self.insensitive = "UNKOWN"
        self.new_file_1 = "case-sensitive.txt.tmp"
        self.new_file_2 = "CASE-SENSITIVE.TXT.TMP"

    def validate(self, value):
        logging.info("validate")

    def check(self, path):
        count = 0
        if len(str(path)):
            pass
        else:
            path = os.path.expanduser('~') + '/Test'
        self.new_file_1 = Path(os.path.join(path), self.new_file_1)
        self.new_file_2 = Path(os.path.join(path), self.new_file_2)
        try:
            f1 = open(self.new_file_1, "x")
            if f1:
                f1.close()
            else:
                raise FileExistsError()
        except FileExistsError:
            logging.info(f"File '{self.new_file_1}' already exists.")
        else:
            count += 1
            logging.info(f"File '{self.new_file_1}' created.")

        try:
            f2 = open(self.new_file_2, "x")
            if f2:
                f2.close()
            else:
                raise FileExistsError()
        except FileExistsError:
            logging.info(f"File '{self.new_file_2}' already exists.")
        else:
            count += 1
            logging.info(f"File '{self.new_file_2}' created.")

        logging.info('count: %s', count)
        if count == 2:
            self.insensitive = "NO"
            os.remove(self.new_file_1)
            os.remove(self.new_file_2)
        elif count == 1:
            self.insensitive = "YES"
            os.remove(self.new_file_1)

        return self.insensitive
