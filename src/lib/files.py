import os, re, logging
from pathlib import Path
from abc import ABC, abstractmethod  # import Abstract Base Classes
from PySide6.QtCore import Slot
from lib.exceptions import AppError


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

    def __init__(self, ui):
        logging.info("Files __init__")
        self.filelist = []  # List of files in directory
        self.changed = {}
        self.file = dict(path="", base="", dir="", name="", ext="", id="",
                         brackets=False, brackets_only=False, new="")        
        self.limit = 1000  # max number in self.filelist
        self.separator = r"[- \.]"  # hyphen or space or dot

        self.app_error = AppError()
        self.error = dict(name="", exit=True, err="", file="")

        # Regex id
        self.regexid = r'\[.+\]'

    def validate(self, value):
        print("validate")

    def __iter__(self):
        self.filelist = []
        return self

    @Slot()
    def print_title(self, title, ui, widget):
        logging.info("Print Title")
        ui.dir_output.clear()
        text = '<span style="font-weight: bold">' + title + '</span>'
        ui.dir_output.append(text)
        ui.dir_output.append("")

    def find(self, path, ui, widget):
        self.filelist.clear()
        self.changed.clear()
        count = 0
        try:
            if ui.recursively.isChecked():
                for file in Path(path).rglob('*'):
                    if os.path.isfile(file):
                        if count <= self.limit:
                            # self.filelist.append(os.path.join(path, file))
                            self.filelist.append(file)
                            count += 1
                        else:
                            self.filelist.clear()
                            ui.dir_output.clear()
                            raise AppError()
            else:
                for file in Path(path).iterdir():
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
            ui.rename_btn.setEnabled(False)
            self.filelist.clear()
            ui.dir_output.clear()
            text = '<span style="color: red; font-weight: bold">NO FILES FOUND!</span>'
            ui.dir_output.append(text)
        except AppError:
            self.filelist.clear()
            msg = 'FILE LIMIT REACHED: ' + str(self.limit)
            self.app_error.print(ui, msg)
        else:
            self.filelist.sort()

    @Slot()
    def list(self, path, ui, widget):
        text = ""
        if self.filelist:
            title = "List Files"
            self.print_title(title, ui, widget)
            for file in self.filelist:
                ui.dir_output.append(os.path.basename(file))
            ui.dir_output.append("")
            text = 'Total Files: ' + str(len(self.filelist))
            ui.dir_output.append(text)
            ui.dir_output.append("")

    def split_name(self, path, ui, widget, title):
        logging.info("Split Name")
        filename = ""
        try:
            if os.path.exists(path):
                base = os.path.basename(path)
                split_tup = os.path.splitext(base)
                self.file["path"] = path
                self.file["base"] = base
                self.file["dir"] = os.path.dirname(path)
                self.file["name"] = split_tup[0]
                self.file["ext"] = split_tup[1]

                filename = ""
                if ui.extension.isChecked():
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
    def compare(self, file, data, ui, widget, title):
        logging.info("Compare")
        logging.info("file: %s", file)
        logging.info("data: %s", data)
        new_file = ""
        text = ""
        if ui.extension.isChecked():
            if file["name"] != file["new"] and file['new'] != "":
                new_file = file["new"] + file["ext"]
        else:
            if file["base"] != file["new"] and file['new'] != "":
                new_file = file["new"]
        new_file = os.path.join(file["dir"], new_file)
        if os.path.exists(new_file) is False:
            data["count"] += 1
            num = data["count"]
            self.changed[num] = {}
            self.changed[num]['path'] = file['path']
            self.changed[num]['new'] = new_file
            logging.info('data["count"]: %s', data["count"])
            text = '<span style="color: blue; font-weight: bold;">Preview</span>'
            ui.dir_output.append(text)
            ui.dir_output.append(os.path.basename(file["path"]))
            ui.dir_output.append(os.path.basename(new_file))
            ui.dir_output.append("")

    @Slot()
    def rename(self, path, ui, widget, title):
        logging.info("Rename")
        count = 0
        for key in self.changed.keys():
            if os.path.exists(self.changed[key]['new']):
                logging.info("File already exists!")
            else:
                os.replace(self.changed[key]['path'], self.changed[key]['new'])
                count += 1
                text = '<span style="color: red; font-weight: bold;">Renamed</span>'
                ui.dir_output.append(text)
                ui.dir_output.append(os.path.basename(self.changed[key]['path']))
                ui.dir_output.append(os.path.basename(self.changed[key]['new']))
                ui.dir_output.append("")
                ui.rename_btn.setEnabled(False)

    @Slot()
    def preview(self, data, ui, widget, title):
        logging.info("Preview")
        logging.info('data: %s', data)
        if data["count"] == 0:
            ui.dir_output.append("No changes")
            ui.dir_output.append("")
            ui.rename_btn.setEnabled(False)
        elif data["count"] > 0:
            ui.rename_btn.setEnabled(True)
        else:
            logging.info("Nada")
