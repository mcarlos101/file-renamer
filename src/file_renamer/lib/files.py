import os
import re
import logging
from pathlib import Path
import os.path
from abc import ABC, abstractmethod
from PySide6.QtCore import Slot
from file_renamer.lib.exceptions import AppError
from file_renamer.lib.case_insensitive import CaseInsensitive


class File(ABC):

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


class Files(File):

    def __init__(self, **params):
        self.name = "MainWindow"
        self.params = params
        logging.info('files.py')
        logging.info('%s%s()', self.params['tab'], self.name)
        self.filelist = []  # List of files in directory
        self.changed = {}
        self.file = dict(
            path="", base="", dir="", name="", ext="", id="", new="",
            current=""
        )
        self.limit = 1000  # max number in self.filelist
        self.separator = r"[- \.]"  # hyphen or space or dot

        self.app_error = AppError()
        self.error = dict(name="", exit=True, err="", file="")

        # Regex id
        self.regexid = r'\[.+\]'

        # Check case insensitive file systems such as Windows & macOS
        self.case_insensitive = CaseInsensitive()
        self.case_insensitive_val = "UNKOWN"

    def validate(self, value):
        logging.info("validate")

    def __iter__(self):
        self.filelist = []
        return self

    @Slot()
    def print_title(self, **params):
        logging.info('%s%s.print_title()', self.params['tab'], self.name)
        self.params = params
        logging.info("Print Title")
        logging.info('self.params: %s', self.params)
        self.params["ui"].dir_output.clear()
        text = '<span style="font-weight: bold">' + self.params["title"] + \
               '</span>'
        self.params["ui"].dir_output.append(text)
        self.params["ui"].dir_output.append("")

    def find(self, **params):
        logging.info('%s%s.find()', self.params['tab'], self.name)
        self.params = params
        self.filelist.clear()
        self.changed.clear()
        count = 0
        try:
            if self.params["ui"].recursively.isChecked():
                for file in Path(params["path"]).rglob('*'):
                    if os.path.isfile(file):
                        if count <= self.limit:
                            self.filelist.append(file)
                            count += 1
                        else:
                            self.filelist.clear()
                            self.params["ui"].dir_output.clear()
                            raise AppError()
            else:
                for file in Path(params["path"]).iterdir():
                    if os.path.isfile(file):
                        if count <= self.limit:
                            self.filelist.append(file)
                            count += 1
                        else:
                            self.filelist.clear()
                            raise AppError()
            if count == 0:
                raise FileNotFoundError()
        except FileNotFoundError:
            self.params["ui"].rename_btn.setEnabled(False)
            self.filelist.clear()
            self.params["ui"].dir_output.clear()
            text = '<span style="color: red; font-weight: bold">' + \
                   'NO FILES FOUND!</span>'
            self.params["ui"].dir_output.append(text)
        except AppError:
            self.filelist.clear()
            self.params["msg"] = 'FILE LIMIT REACHED: ' + str(self.limit)
            # msg = 'FILE LIMIT REACHED: ' + str(self.limit)
            self.app_error.print(**params)
        else:
            self.filelist.sort()
            self.params["case_insensitive_val"] = \
                self.case_insensitive.check(params["path"])
            logging.info(
                'self.params["case_insensitive_val"]: %s',
                self.params["case_insensitive_val"]
            )

    @Slot()
    def list(self, **params):
        logging.info('%s%s.list()', self.params['tab'], self.name)
        self.params = params
        text = ""
        if self.filelist:
            self.params["title"] = "List Files"
            self.print_title(**params)
            for file in self.filelist:
                self.params["ui"].dir_output.append(str(file))
            self.params["ui"].dir_output.append("")
            text = 'Total Files: ' + str(len(self.filelist))
            self.params["ui"].dir_output.append(text)
            self.params["ui"].dir_output.append("")

    def split_name(self, **params):
        logging.info('%s%s.split_name()', self.params['tab'], self.name)
        self.params = params
        logging.info('%sself.params: %s', self.params['tab'], self.params)
        filename = ""
        try:
            if os.path.exists(params["filename"]):
                self.file["path"] = self.params["filename"]
                self.file["base"] = os.path.basename(params["filename"])
                self.file["dir"] = os.path.dirname(params["filename"])
                split_tup = os.path.splitext(self.file["base"])
                self.file["name"] = split_tup[0]
                self.file["ext"] = split_tup[1]

                filename = ""
                if self.params["ui"].extension.isChecked():
                    filename = self.file['name']
                else:
                    filename = self.file['base']
                result = re.search(self.regexid, filename)
                if result:
                    self.file['id'] = result.group()
                else:
                    self.file['id'] = ""
            else:
                raise FileNotFoundError()
        except FileNotFoundError:
            logging.info("FileNotFoundError")
            return None
        else:
            return self.file

    @Slot()
    def compare(self, file, data, **params):
        logging.info('%s%s.compare()', self.params['tab'], self.name)
        self.params = params
        logging.info("%sdata: %s", self.params['tab'], data)
        file["current"] = ""
        text = ""
        file_exists = True
        logging.info('%sfile["name"]: %s', self.params['tab'], file["name"])
        logging.info('%sfile["base"]: %s', self.params['tab'], file["base"])
        logging.info('%sfile["new"] : %s', self.params['tab'], file["new"])
        logging.info('%sfile["dir"] : %s', self.params['tab'], file["dir"])
        logging.info(
            '%sself.params["ui"].extension.isChecked(): %s',
            self.params['tab'],
            self.params["ui"].extension.isChecked()
        )
        if self.params["ui"].extension.isChecked():
            if file["name"] != file["new"] and file['new'] != "":
                file["current"] = file["name"] + file["ext"]
        else:
            if file["base"] != file["new"] and file['new'] != "":
                file["current"] = file["base"]
            else:
                file["current"] = file["base"]

        logging.info(
            '%sfile["current"]: %s',
            self.params['tab'],
            file["current"]
        )
        logging.info(
            '%sself.case_insensitive_val: %s',
            self.params['tab'],
            self.case_insensitive_val
        )
        if self.case_insensitive_val:
            logging.info(
                '%sfile["current"].lower(): %s',
                self.params['tab'],
                file["current"].lower()
            )
            logging.info(
                '%sfile["new"].lower()    : %s',
                self.params['tab'],
                file["new"].lower()
            )
            if file["current"] == file["new"]:
                logging.info('%sNo change', self.params['tab'])
                file_exists = True
            elif file["current"] != file["new"]:
                logging.info('%sChanged', self.params['tab'])
                # Track lower or title case change
                logging.info(
                    '%sself.params["case_change"]: %s',
                    self.params['tab'],
                    self.params["case_change"]
                )
                if self.params["case_change"]:
                    if file["current"].lower() == file["new"].lower():
                        file_exists = False
                        logging.info(
                            '%sfile_exists: %s',
                            self.params['tab'],
                            file_exists
                        )
                    elif file["current"].lower() != file["new"].lower():
                        file_exists = False
                        logging.info(
                            '%sfile_exists: %s',
                            self.params['tab'],
                            file_exists
                        )
                else:
                    file_exists = False
                    logging.info(
                        '%sfile_exists: %s',
                        self.params['tab'],
                        file_exists
                    )
        else:
            file_exists = os.path.exists(
                (Path(os.path.join(file["dir"]), file["new"]))
            )
            logging.info(
                '%sfile_exists full path: %s',
                self.params['tab'],
                file_exists
            )

        logging.info('file_exists: %s', file_exists)
        if file_exists is False:
            data["count"] += 1
            num = data["count"]
            self.changed[num] = {}
            self.changed[num]["path"] = Path(
                os.path.join(file["dir"]), file["current"]
            )
            self.changed[num]["new"] = Path(
                os.path.join(file["dir"]), file["new"]
            )
            logging.info(
                '%sself.changed[num]["path"]: %s',
                self.params['tab'],
                self.changed[num]["path"]
            )
            logging.info(
                '%sself.changed[num]["new"]: %s',
                self.params['tab'],
                self.changed[num]["new"]
            )
            logging.info(
                '%sdata["count"]: %s',
                self.params['tab'],
                data["count"]
            )
            text = '<span style="color: blue; font-weight: bold;">' + \
                'Preview</span>'
            self.params["ui"].dir_output.append(text)
            self.params["ui"].dir_output.append(str(self.changed[num]["path"]))
            self.params["ui"].dir_output.append(str(self.changed[num]["new"]))
            self.params["ui"].dir_output.append("")

    @Slot()
    def rename(self, **params):
        logging.info('%s%s.rename()', self.params['tab'], self.name)
        self.params = params
        count = 0
        current_file = ""
        new_file = ""
        for key in self.changed.keys():
            current_file = self.changed[key]['path']
            new_file = self.changed[key]['new']
            if self.case_insensitive_val:
                tmp_file = str(current_file) + '.tmp'
                os.replace(current_file, tmp_file)
                os.replace(tmp_file, new_file)
            else:
                os.replace(current_file, new_file)
            count += 1
            text = '<span style="color: red; font-weight: bold;">' + \
                'Renamed</span>'
            self.params["ui"].dir_output.append(text)
            self.params["ui"].dir_output.append(
                os.path.basename(self.changed[key]['path'])
            )
            self.params["ui"].dir_output.append(
                os.path.basename(self.changed[key]['new'])
            )
            self.params["ui"].dir_output.append("")
            self.params["ui"].rename_btn.setEnabled(False)

    @Slot()
    def preview(self, data, **params):
        logging.info('%s%s.preview()', self.params['tab'], self.name)
        self.params = params
        logging.info('%sdata: %s', self.params['tab'], data)
        if data["count"] == 0:
            self.params["ui"].dir_output.append("No changes")
            self.params["ui"].dir_output.append("")
            self.params["ui"].rename_btn.setEnabled(False)
        elif data["count"] > 0:
            self.params["ui"].rename_btn.setEnabled(True)
        else:
            logging.info('%sUnkown', self.params['tab'])
