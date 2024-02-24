import os, re, logging
import unidecode
from pathlib import Path

from lib.files import Files
from lib.exceptions import AppError


class Rename:

    def __init__(self, name, platform, ui):
        """The __init__ method is a constructor"""
        self.logfile = os.path.expanduser('~') + "/rename.log"
        logging.basicConfig(filename=self.logfile, filemode='w',
                            level=logging.INFO)
        logging.info("Rename __init__")
        self.name = name
        self.platform = platform
        self.files = Files(platform, ui)
        self.file = {}
        self.data = {
            "preview": True,
            "count": 0
        }
        self.chars = [' ', '.', '-', '_', '[', ']']  # Chars allowed
        self.app_error = AppError()

    def list_files(self, path, ui, widget):
        self.files.find(path, ui, widget)
        self.files.list(path, ui, widget)

    def check_options(self, ui, widget):
        filename = ""

        if ui.extension.isChecked():
            filename = self.file['name']
        else:
            filename = self.file['base']

        # Keep id
        if ui.id.isChecked():
            filename = filename.replace(self.file['id'], "")
        else:
            pass

        if ui.extension.isChecked() and ui.id.isChecked():
            filename = self.file['name']
            filename = filename.replace(self.file['id'], "")
        else:
            pass

        return filename


    def update_options(self, ui, widget):
        logging.info("self.file['new']: %s", self.file['new'])
        if self.file['new'] != "":
            if ui.extension.isChecked() and ui.id.isChecked():
                self.file['new'] = self.file['new'] + self.file['id'] + self.file['ext']

            elif ui.extension.isChecked() and ui.id.isChecked() is False:
                self.file['new'] = self.file['new'] + self.file['ext']

            elif ui.extension.isChecked() is False and ui.id.isChecked():
                index = self.file['new'].find(self.file['ext'])
                self.file['new'] = self.file['new'][:index] + self.file['id'] + self.file['new'][index:]

            elif ui.extension.isChecked() is False and ui.id.isChecked() is False:
                pass

            else:
                pass
        else:
            pass

    def remove_chars(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        msg = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = ""
                logging.info('filename: %s', filename)
                for elem in filename:
                    if elem.isalnum() or elem in self.chars:
                        self.file['new'] += elem

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except AppError:
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def remove_accents(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = ""
                for i in range(len(filename)):
                    # remove ascents
                    self.file['new'] += unidecode.unidecode(filename[i])

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

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

    def trim_spaces(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = filename.strip()
                self.file['new'] = self.replace_dup_dots_w_spaces(
                    self.file['new'])
                self.file['new'] = self.remove_dup_spaces(self.file['new'])

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def replace_spaces(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = self.replace_spaces_w_hyphens(
                    filename)
                self.file['new'] = self.replace_underscores_w_hyphens(
                    self.file['new'])
                self.file['new'] = self.remove_dup_hyphens(
                    self.file['new'])

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def replace_dots(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = self.replace_dots_w_hyphens(
                    filename)

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def replace_hyphens(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = self.replace_hyphens_w_spaces(
                    filename)

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def lower_case(self, path, ui, widget, title, case_change):
        logging.info(title)
        logging.info('path: %s', path)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = filename.lower()

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def title_case(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                self.file['new'] = filename.title()

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def remove_ids(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        regex = ""
        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                if len(self.file['id']):
                    regex = (r'([- \.]' + re.escape(self.file['id']) + r')')
                    logging.info('regex: %s', regex)
                    result = re.search(regex, filename)

                    logging.info('result: %s', result)
                    if result:
                        logging.info('result.group(0): %s', result.group(0))
                        self.file['new'] = filename.replace(result.group(0), "")
                    else:
                        self.file['new'] = filename
                else:
                    self.file['new'] = filename

                self.update_options(ui, widget)

                self.files.compare(self.file, self.data, ui, widget, title, case_change)
        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def search_replace(self, path, ui, widget, title, case_change):
        logging.info(title)
        self.data['count'] = 0
        self.files.print_title(title, ui, widget)
        self.files.find(path, ui, widget)
        filename = ""
        pattern = ''
        replace = ''

        # Metachars
        char = [".", "^", "$", "*", "+", "?", "{", "}", "[", "]" "\\", "|"]
        char.append("(")
        char.append(")")
        logging.info('char: %s', char)

        try:
            for f in self.files.filelist:
                logging.info("------------------------------")
                logging.info('Path(f)   : %s', Path(f))
                self.file.clear()
                self.file = self.files.split_name(f, ui, widget, title)

                filename = self.check_options(ui, widget)

                if len(ui.search.displayText()):
                    pattern = ui.search.displayText()

                if ui.regex.isChecked():
                    logging.info('pattern: %s', pattern)
                    p = re.compile(pattern)

                    result = p.search(filename)
                    if result:
                        logging.info('result.group(): %s', result.group())
                        replace = ui.replace.displayText()
                        raw_replace = repr(replace)[1:-1] # raw string
                        self.file['new'] = filename.replace(result.group(),
                                                            raw_replace, 1)
                    else:
                        self.file['new'] = filename
                else:
                    logging.info('pattern: %s', pattern)
                    p = re.compile(re.escape(pattern))
                    result = p.search(filename)
                    if result:
                        logging.info('result.group(): %s', result.group())
                        replace = ui.replace.displayText()
                        logging.info('replace: %s', replace)
                        self.file['new'] = filename.replace(result.group(), replace)
                    else:
                        self.file['new'] = filename

                self.update_options(ui, widget)
                self.files.compare(self.file, self.data, ui, widget, title, case_change)

        except SystemError:
            self.files.filelist.clear()
            msg = 'SystemError'
            self.app_error.print(ui, msg)
        else:
            self.files.preview(self.data, ui, widget, title)

    def rename_files(self, path, ui, widget, title, case_change):
        self.files.print_title(title, ui, widget)
        self.files.rename(path, ui, widget, title)
