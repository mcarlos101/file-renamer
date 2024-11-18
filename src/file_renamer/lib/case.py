import os
import logging
import inspect
from pathlib import Path
from abc import ABC, abstractmethod


class Case(ABC):

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


class CaseSensitive(Case):

    def __init__(self, **fr):
        self.fr = fr
        self.case_sensitive_val = False
        self.write = False  # File system write permission
        self.new_file_1 = "case-sensitive.txt.tmp"
        self.new_file_2 = "CASE-SENSITIVE.TXT.TMP"

    def validate(self, value):
        pass

    def check(self, path):
        count = 0  # Num of files created
        self.new_file_1 = Path(os.path.join(path), self.new_file_1)
        self.new_file_2 = Path(os.path.join(path), self.new_file_2)
        if self.fr['write'] is False:
            try:
                with open(self.new_file_1, 'x') as f1:
                    count += 1
                    self.write = True
                    self.fr["write"] = self.write
                    logging.info('self.fr["write"]: %s', self.fr["write"])
                    logging.info(f"File '{self.new_file_1}' created")
            except FileExistsError:
                logging.info(f"File '{self.new_file_1}' already exists")
            try:
                with open(self.new_file_2, 'x') as f2:
                    count += 1
                    logging.info(f"File '{self.new_file_2}' created")
            except FileExistsError:
                logging.info(f"File '{self.new_file_2}' already exists")
            logging.info('count: %s', count)
            if count == 2:
                self.case_sensitive_val = True
                self.fr['case_sensitive'] = self.case_sensitive_val
                logging.info(
                    'self.case_sensitive_val: %s', self.case_sensitive_val
                )
                os.remove(self.new_file_1)
                os.remove(self.new_file_2)
                logging.info(f"File '{self.new_file_1}' deleted")
                logging.info(f"File '{self.new_file_2}' deleted")
            elif count == 1:
                self.case_sensitive_val = False
                logging.info(
                    'self.case_sensitive_val: %s', self.case_sensitive_val
                )
                os.remove(self.new_file_1)
                logging.info(f"File '{self.new_file_1}' deleted")
        return self.case_sensitive_val
