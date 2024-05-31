import sys
import re
import logging
import unidecode
from pathlib import Path
from file_renamer.lib.files import Files
from file_renamer.lib.exceptions import AppError


class Rename:

    def __init__(self, **params):
        """The __init__ method is a constructor"""
        self.name = "Rename"
        self.params = params
        logging.info('rename.py')
        logging.info('%s%s()', self.params['tab'], self.name)
        logging.info('%sself.params: %s', self.params['tab'], self.params)

        # self.platform = platform
        self.files = Files(**self.params)
        self.file = {}
        self.data = {
            "preview": True,
            "count": 0
        }
        self.chars = [' ', '.', '-', '_', '[', ']']  # Chars allowed
        self.app_error = AppError()

    def list_files(self, **params):
        logging.info('%s%s.list_files()', self.params['tab'], self.name)
        self.params = params
        self.files.find(**self.params)
        self.files.list(**self.params)

    def check_options(self, **params):
        logging.info('%s%s.check_options()', self.params['tab'], self.name)
        self.params = params
        filename = ""

        if self.params["ui"].extension.isChecked():
            filename = self.file['name']
        else:
            filename = self.file['base']

        # Keep id
        if self.params["ui"].id.isChecked():
            filename = filename.replace(self.file['id'], "")
        else:
            pass

        if self.params["ui"].extension.isChecked() and self.params["ui"].id.isChecked():
            filename = self.file['name']
            filename = filename.replace(self.file['id'], "")
        else:
            pass

        return filename

    def update_options(self, **params):
        self.params = params
        logging.info('%s%s.update_options()', self.params['tab'], self.name)
        logging.info("self.file['new']: %s", self.file['new'])
        if self.file['new'] != "":
            if (params["ui"].extension.isChecked() and
                    self.params["ui"].id.isChecked()):
                self.file['new'] = self.file['new'] + self.file['id'] + \
                    self.file['ext']

            elif self.params["ui"].extension.isChecked() and \
                    self.params["ui"].id.isChecked() is False:
                self.file['new'] = self.file['new'] + self.file['ext']

            elif self.params["ui"].extension.isChecked() is False and \
                    self.params["ui"].id.isChecked():
                index = self.file['new'].find(self.file['ext'])
                self.file['new'] = self.file['new'][:index] + self.file['id'] \
                    + self.file['new'][index:]

            elif self.params["ui"].extension.isChecked() is False and \
                    self.params["ui"].id.isChecked() is False:
                pass

            else:
                pass
        else:
            pass

    def remove_chars(self, **params):
        logging.info('%s%s.remove_chars()', self.params['tab'], self.name)
        self.params = params
        logging.info(params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)
                logging.info('self.file: %s', self.file)

                filename2 = self.check_options(**self.params)

                self.file['new'] = ""
                logging.info('filename2: %s', filename2)
                for elem in filename2:
                    if elem.isalnum() or elem in self.chars:
                        self.file['new'] += elem

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except AppError:
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def remove_accents(self, **params):
        logging.info('%s%s.remove_accents()', self.params['tab'], self.name)
        self.params = params
        logging.info(params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                self.file['new'] = ""
                for i in range(len(filename2)):
                    # remove ascents
                    self.file['new'] += unidecode.unidecode(filename2[i])

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    @staticmethod
    def remove_dots(string):
        pattern = re.compile(r'\.')
        return re.sub(pattern, '', string)

    @staticmethod
    def replace_dup_dots_w_spaces(string):
        pattern = re.compile(r'\.{2,}')
        return re.sub(pattern, ' ', string)

    @staticmethod
    def replace_dots_w_hyphens(string):
        pattern = re.compile(r'\.{1,}')
        return re.sub(pattern, '-', string)

    @staticmethod
    def replace_underscores_w_hyphens(string):
        pattern = re.compile(r'_')
        return re.sub(pattern, '-', string)

    @staticmethod
    def remove_dup_spaces(string):
        pattern = re.compile(r'\s{2,}')
        return re.sub(pattern, ' ', string)

    @staticmethod
    def replace_spaces_w_hyphens(string):
        pattern = re.compile(r'\s')
        return re.sub(pattern, '-', string)

    @staticmethod
    def remove_dup_hyphens(string):
        pattern = re.compile(r'-{2,}')
        return re.sub(pattern, '-', string)

    @staticmethod
    def replace_hyphens_w_spaces(string):
        pattern = re.compile(r'-{1,}')
        return re.sub(pattern, ' ', string)

    def trim_spaces(self, **params):
        self.params = params
        logging.info(params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                self.file['new'] = filename2.strip()
                self.file['new'] = self.replace_dup_dots_w_spaces(
                    self.file['new'])
                self.file['new'] = self.remove_dup_spaces(self.file['new'])

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def replace_spaces(self, **params):
        self.params = params
        logging.info(params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                self.file['new'] = self.replace_spaces_w_hyphens(
                    filename2)
                """
                self.file['new'] = self.replace_underscores_w_hyphens(
                    self.file['new'])
                """
                self.file['new'] = self.remove_dup_hyphens(
                    self.file['new'])

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def replace_dots(self, **params):
        self.params = params
        logging.info(params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                self.file['new'] = self.replace_dots_w_hyphens(
                    filename2)

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def replace_hyphens(self, **params):
        self.params = params
        logging.info(params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                self.file['new'] = self.replace_hyphens_w_spaces(
                    filename2)

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def lower_case(self, **params):
        self.params = params
        logging.info('self.params["title"]: %s', self.params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                self.file['new'] = filename2.lower()

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def title_case(self, **params):
        self.params = params
        logging.info('self.params["title"]: %s', self.params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                self.file['new'] = filename2.title()

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def remove_ids(self, **params):
        self.params = params
        logging.info('self.params["title"]: %s', self.params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        regex = ""
        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

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

                self.update_options(**self.params)

                self.files.compare(self.file, self.data, **self.params)
        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def search_replace(self, **params):
        self.params = params
        logging.info('self.params["title"]: %s', self.params["title"])
        self.data['count'] = 0
        self.files.print_title(**self.params)
        self.files.find(**self.params)
        filename = ""
        filename2 = ""
        self.params["msg"] = ""
        pattern = ''
        replace = ''

        try:
            for filename in self.files.filelist:
                logging.info("------------------------------")
                self.params["filename"] = Path(filename)
                logging.info('params["filename"]: %s', self.params["filename"])
                self.file.clear()
                self.file = self.files.split_name(**self.params)

                filename2 = self.check_options(**self.params)

                if len(params["ui"].search.displayText()):
                    pattern = self.params["ui"].search.displayText()

                if self.params["ui"].regex.isChecked():
                    logging.info('pattern: %s', pattern)
                    p = re.compile(pattern)

                    result = p.search(filename2)
                    if result:
                        logging.info('result.group(): %s', result.group())
                        replace = self.params["ui"].replace.displayText()
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
                        replace = self.params["ui"].replace.displayText()
                        logging.info('replace: %s', replace)
                        self.file['new'] = filename2.replace(
                            result.group(),
                            replace
                        )
                    else:
                        self.file['new'] = filename2

                self.update_options(**self.params)
                self.files.compare(self.file, self.data, **self.params)

        except SystemError:
            self.files.filelist.clear()
            self.params["msg"] = 'SystemError'
            self.app_error.print(**self.params)
        else:
            self.files.preview(self.data, **self.params)

    def rename_files(self, **params):
        self.params = params
        self.files.print_title(**self.params)
        self.files.rename(**self.params)
