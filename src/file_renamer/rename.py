import sys
import re
import logging
import unidecode
import inspect
from pathlib import Path
from file_renamer.lib.files import Files
from file_renamer.lib.exceptions import Messages


class Rename:

    def __init__(self, **fr):
        """The __init__ method is a constructor"""

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.fr = fr
        logging.info('fr: %s', fr)

        self.files = Files(**self.fr)
        self.file = {}
        self.data = {
            "preview": True,
            "count": 0
        }
        self.chars = [' ', '.', '-', '_', '[', ']']  # Chars allowed

    def list_files(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.files.find(**self.fr)
        self.files.list(**self.fr)

    def check_options(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        filename = ""

        if self.fr["ui"].extension.isChecked():
            filename = self.file['name']
        else:
            filename = self.file['base']

        # Keep id
        if self.fr["ui"].id.isChecked():
            filename = filename.replace(self.file['id'], "")
        else:
            pass

        if self.fr["ui"].extension.isChecked() and \
                self.fr["ui"].id.isChecked():
            filename = self.file['name']
            filename = filename.replace(self.file['id'], "")
        else:
            pass

        return filename

    def update_options(self, **fr):
        self.fr = fr
        logging.info(inspect.stack()[0].function)  # method name
        logging.info("self.file['new']: %s", self.file['new'])
        if self.file['new'] != "":
            if (fr["ui"].extension.isChecked() and
                    self.fr["ui"].id.isChecked()):
                self.file['new'] = self.file['new'] + self.file['id'] + \
                    self.file['ext']

            elif self.fr["ui"].extension.isChecked() and \
                    self.fr["ui"].id.isChecked() is False:
                self.file['new'] = self.file['new'] + self.file['ext']

            elif self.fr["ui"].extension.isChecked() is False and \
                    self.fr["ui"].id.isChecked():
                index = self.file['new'].find(self.file['ext'])
                self.file['new'] = self.file['new'][:index] + self.file['id'] \
                    + self.file['new'][index:]

            elif self.fr["ui"].extension.isChecked() is False and \
                    self.fr["ui"].id.isChecked() is False:
                pass

            else:
                pass
        else:
            pass

    def remove_chars(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)
                logging.info('self.file: %s', self.file)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = ""
                logging.info('filename2: %s', filename2)
                for elem in filename2:
                    if elem.isalnum() or elem in self.chars:
                        self.file['new'] += elem

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except Errors as err:
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def remove_accents(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = ""
                for i in range(len(filename2)):
                    # remove ascents
                    self.file['new'] += unidecode.unidecode(filename2[i])

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    @staticmethod
    def remove_dots(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'\.')
        return re.sub(pattern, '', string)

    @staticmethod
    def replace_dup_dots_w_spaces(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'\.{2,}')
        return re.sub(pattern, ' ', string)

    @staticmethod
    def replace_dots_w_hyphens(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'\.{1,}')
        return re.sub(pattern, '-', string)

    @staticmethod
    def replace_underscores_w_hyphens(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'_')
        return re.sub(pattern, '-', string)

    @staticmethod
    def remove_dup_spaces(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'\s{2,}')
        return re.sub(pattern, ' ', string)

    @staticmethod
    def replace_spaces_w_hyphens(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'\s')
        return re.sub(pattern, '-', string)

    @staticmethod
    def remove_dup_hyphens(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'-{2,}')
        return re.sub(pattern, '-', string)

    @staticmethod
    def replace_hyphens_w_spaces(string):
        logging.info(inspect.stack()[0].function)  # method name
        pattern = re.compile(r'-{1,}')
        return re.sub(pattern, ' ', string)

    def trim_spaces(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = filename2.strip()
                self.file['new'] = self.replace_dup_dots_w_spaces(
                    self.file['new'])
                self.file['new'] = self.remove_dup_spaces(self.file['new'])

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def replace_spaces(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = self.replace_spaces_w_hyphens(
                    filename2)
                """
                self.file['new'] = self.replace_underscores_w_hyphens(
                    self.file['new'])
                """
                self.file['new'] = self.remove_dup_hyphens(
                    self.file['new'])

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def replace_dots(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = self.replace_dots_w_hyphens(
                    filename2)

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def replace_hyphens(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = self.replace_hyphens_w_spaces(
                    filename2)

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def lower_case(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = filename2.lower()

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def title_case(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                self.file['new'] = filename2.title()

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def remove_ids(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        regex = ""
        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                if len(self.file['id']):
                    regex = (r'([- \.]' + re.escape(self.file['id']) + r')')
                    logging.info('regex: %s', regex)
                    result = re.search(regex, filename2)

                    logging.info('result: %s', result)
                    if result:
                        logging.info('result.group(0): %s', result.group(0))
                        self.file['new'] = filename2.replace(
                            result.group(0), ""
                        )
                    else:
                        self.file['new'] = filename2
                else:
                    self.file['new'] = filename2

                self.update_options(**self.fr)

                self.files.compare(self.file, self.data, **self.fr)
        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def search_replace(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.data['count'] = 0
        self.files.print_title(**self.fr)
        self.files.find(**self.fr)
        filename = ""
        filename2 = ""
        pattern = ''
        replace = ''

        try:
            for filename in self.files.filelist:
                self.fr["filename"] = Path(filename)
                logging.info('fr["filename"]: %s', self.fr["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.fr)

                filename2 = self.check_options(**self.fr)

                if len(fr["ui"].search.displayText()):
                    pattern = self.fr["ui"].search.displayText()

                if self.fr["ui"].regex.isChecked():
                    logging.info('pattern: %s', pattern)
                    p = re.compile(pattern)

                    result = p.search(filename2)
                    if result:
                        logging.info('result.group(): %s', result.group())
                        replace = self.fr["ui"].replace.displayText()
                        raw_replace = repr(replace)[1:-1]  # raw string
                        self.file['new'] = re.sub(pattern, replace, filename2)
                    else:
                        self.file['new'] = filename2
                else:
                    logging.info('pattern: %s', pattern)
                    p = re.compile(re.escape(pattern))
                    result = p.search(filename2)
                    if result:
                        logging.info('result.group(): %s', result.group())
                        replace = self.fr["ui"].replace.displayText()
                        logging.info('replace: %s', replace)
                        self.file['new'] = filename2.replace(
                            result.group(),
                            replace
                        )
                    else:
                        self.file['new'] = filename2

                self.update_options(**self.fr)
                self.files.compare(self.file, self.data, **self.fr)

        except SystemError as err:
            self.files.filelist.clear()
            self.fr['msg-info'] = err
            msg = Messages(**self.fr)
        else:
            self.files.preview(self.data, **self.fr)

    def rename_files(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.files.print_title(**self.fr)
        self.files.rename(**self.fr)
