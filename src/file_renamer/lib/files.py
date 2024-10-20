import os
import re
import logging
import inspect
import os.path
from pathlib import Path
from abc import ABC, abstractmethod
from PySide6.QtCore import Slot
from file_renamer.lib.exceptions import Messages
from file_renamer.lib.case import CaseSensitive


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

    def __init__(self, **fr):

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.fr = fr
        logging.info('fr: %s', fr)

        self.filelist = []  # List of files in directory
        self.changed = {}
        self.file = dict(
            path="", base="", dir="", name="", ext="", id="", new="",
            current=""
        )
        self.limit = 1000  # max number in self.filelist
        self.separator = r"[- \.]"  # hyphen or space or dot

        # self.error = dict(name="", exit=True, err="", file="")

        # Regex id
        self.regexid = r'\[.+\]'

        # Check case sensitive file systems
        self.case_sensitive = CaseSensitive(**self.fr)
        self.case_sensitive_val = False

    def validate(self, value):
        logging.info(inspect.stack()[0].function)  # method name
        logging.info("validate")

    def __iter__(self):
        logging.info(inspect.stack()[0].function)  # method name
        self.filelist = []
        return self

    @Slot()
    def print_title(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.fr["ui"].dir_output.clear()
        self.fr["ui"].label.setText(self.fr["title"])

    def find(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        self.filelist.clear()
        self.changed.clear()
        count = 0
        try:
            if self.fr["ui"].recursively.isChecked():
                for file in Path(fr["path"]).rglob('*'):
                    if os.path.isfile(file):
                        if count <= self.limit:
                            self.filelist.append(file)
                            count += 1
                        else:
                            self.filelist.clear()
                            self.fr["ui"].dir_output.clear()
                            raise Exception()
            else:
                for file in Path(fr["path"]).iterdir():
                    if os.path.isfile(file):
                        if count <= self.limit:
                            self.filelist.append(file)
                            count += 1
                        else:
                            self.filelist.clear()
                            raise Exception()
            if count == 0:
                raise FileNotFoundError()
        except FileNotFoundError:
            self.fr["ui"].rename_btn.setEnabled(False)
            self.filelist.clear()
            self.fr["ui"].dir_output.clear()
            self.fr['msg-info'] = 'NO FILES FOUND!'
            msg = Messages(**self.fr)
        except Exception:
            self.filelist.clear()
            self.fr['msg-info'] = 'FILE LIMIT REACHED: ' + str(self.limit)
            msg = Messages(**self.fr)

        else:
            self.filelist.sort()
            self.case_sensitive_val = self.case_sensitive.check(fr["path"])
            logging.info(
                'self.case_sensitive_val: %s',
                self.case_sensitive_val
            )

    @Slot()
    def list(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        count = 0
        text = ""
        if self.filelist:
            self.filelist.sort()
            self.fr["title"] = "LIST FILES"
            self.print_title(**fr)
            for file in self.filelist:
                count += 1
                text = "File " + str(count)
                self.fr["ui"].dir_output.append(text)
                self.fr["ui"].dir_output.append(str(file))
                self.fr["ui"].dir_output.append("")
            text = 'Total Files: ' + str(len(self.filelist))
            self.fr["ui"].dir_output.append(text)
            if self.fr['theme'] == 'light':
                self.fr["ui"].label.setStyleSheet(
                    "color: white; background-color: gray;"
                )
            elif self.fr['theme'] == 'dark':
                self.fr["ui"].label.setStyleSheet(
                    "color: white; background-color: black;"
                )

    def split_name(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        filename = ""
        try:
            if os.path.exists(fr["filename"]):
                self.file["path"] = self.fr["filename"]
                self.file["base"] = os.path.basename(fr["filename"])
                self.file["dir"] = os.path.dirname(fr["filename"])
                split_tup = os.path.splitext(self.file["base"])
                self.file["name"] = split_tup[0]
                self.file["ext"] = split_tup[1]

                filename = ""
                if self.fr["ui"].extension.isChecked():
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
            self.fr['msg-info'] = 'FILE NOT FOUND!'
            msg = Messages(**self.fr)
            return None
        else:
            return self.file

    @Slot()
    def compare(self, file, data, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        logging.info("data: %s", data)
        file["current"] = ""
        new_file = ""
        text = ""
        file_exists = False
        file_conflict = False
        logging.info('file["name"]: %s', file["name"])
        logging.info('file["base"]: %s', file["base"])
        logging.info('file["new"] : %s', file["new"])
        logging.info('file["dir"] : %s', file["dir"])
        logging.info(
            'self.fr["ui"].extension.isChecked(): %s',
            self.fr["ui"].extension.isChecked()
        )
        if self.fr["ui"].extension.isChecked():
            if file["name"] != file["new"] and file['new'] != "":
                file["current"] = file["name"] + file["ext"]
        else:
            if file["base"] != file["new"] and file['new'] != "":
                file["current"] = file["base"]
            else:
                file["current"] = file["base"]

        logging.info('file["current"]: %s', file["current"])
        if self.case_sensitive_val is False:
            logging.info(
                'file["current"].lower(): %s',
                file["current"].lower()
            )
            logging.info(
                'file["new"].lower()    : %s',
                file["new"].lower()
            )

        if file["current"] == file["new"]:
            logging.info('No change')
            file_exists = True
            logging.info('1) file_exists: %s', file_exists)
        elif file["current"] != file["new"]:
            logging.info('Changed')
            logging.info('file["current"]: %s', file["current"])
            logging.info('file["new"]: %s', file["new"])

            for filename in self.filelist:
                # filename = os.path.basename(filename)
                logging.info('filename: %s', filename)
                new_file = (Path(os.path.join(file["dir"]), file["new"]))
                logging.info('new_file: %s', new_file)
                logging.info('Path(filename): %s', Path(filename))
                if new_file == Path(filename):
                    file_exists = True
                    logging.info('2) file_exists: %s', file_exists)
                    break
                else:
                    for current_file in self.changed.keys():
                        logging.info('current_file: %s', current_file)
                        if new_file == self.changed[current_file]:
                            file_conflict = True
                            logging.info(
                                'file_conflict: %s',
                                file_conflict
                            )
                            break
            if  self.case_sensitive_val is False:
                if self.fr["case_change"]:
                    if file["current"].lower() == file["new"].lower():
                        file_exists = True
                        logging.info('3) file_exists: %s', file_exists)
                    elif file["current"].lower() != file["new"].lower():
                        file_exists = False
                        logging.info('4) file_exists: %s', file_exists)
                else:
                    pass
            else:
                pass

        if file_exists is False and file_conflict is False:
            data["count"] += 1
            self.changed[self.fr["filename"]] = new_file
            self.fr["ui"].label.setText('PREVIEW -> ' + self.fr["title"])
            self.fr["ui"].label.setStyleSheet(
                "color: white; background-color: #0080ff;"
            )
            text = "Preview " + str(data["count"])
            self.fr["ui"].dir_output.append(text)
            self.fr["ui"].dir_output.append(str(self.fr["filename"]))
            self.fr["ui"].dir_output.append(str(new_file))
            self.fr["ui"].dir_output.append("")

    @Slot()
    def rename(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        count = 0
        current_file = ""
        new_file = ""
        for current_file in self.changed.keys():
            logging.info('current_file: %s', current_file)
            new_file = self.changed[current_file]
            logging.info('new_file: %s', new_file)

            if self.case_sensitive_val:
                tmp_file = str(current_file) + '.tmp'
                os.replace(current_file, tmp_file)
                os.replace(tmp_file, new_file)
            else:
                os.replace(current_file, new_file)
            count += 1
            text = "Renamed " + str(count)
            self.fr["ui"].dir_output.append(text)
            self.fr["ui"].dir_output.append(str(current_file))
            self.fr["ui"].dir_output.append(str(new_file))
            self.fr["ui"].dir_output.append("")
        text = 'Total Files: ' + str(count)
        self.fr["ui"].dir_output.append(text)
        self.fr["ui"].label.setText('RENAMED -> ' + self.fr["title"])
        self.fr["ui"].label.setStyleSheet(
            "color: white; background-color: maroon;"
        )
        self.fr["ui"].rename_btn.setEnabled(False)

    @Slot()
    def preview(self, data, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        self.fr = fr
        logging.info('data: %s', data)
        if data["count"] == 0:
            self.fr["ui"].dir_output.append("No changes")
            self.fr["ui"].dir_output.append("")
            self.fr["ui"].rename_btn.setEnabled(False)
        elif data["count"] > 0:
            text = 'Total Files: ' + str(data["count"])
            self.fr["ui"].dir_output.append(text)
            self.fr["ui"].rename_btn.setEnabled(True)
        else:
            logging.info('data["count"] unknown')
