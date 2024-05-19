# This Python file uses the following encoding: utf-8
import os
import logging
from PySide6.QtWidgets import QWidget, QFileDialog
from pathlib import Path

from file_renamer.rename import Rename
from file_renamer.lib.exceptions import AppError

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
# from ui_form import Ui_Widget
from file_renamer.ui_form import Ui_Widget


class Widget(QWidget):
    def __init__(self, parent=None, **params):
        super().__init__(parent)

        self.params = params

        # Logs
        logging.basicConfig(
            filename=self.params["logs"],
            filemode='w',
            level=logging.INFO
        )
        logging.info("Widget __init__")
        logging.info('self.params["platform"]: %s', self.params["platform"])

        # UI
        self.params["ui"] = Ui_Widget()
        self.params["ui"].setupUi(self)

        # Create rename
        self.rename = Rename(**self.params)

        self.app_error = AppError()

        # Track lower or title case change
        self.params["case_change"] = False

    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.params["path"] = Path(dir_name)
            self.params["ui"].dir_txt.setText(str(self.params["path"]))
            self.rename.list_files(**self.params)

    def add_recursively(self):
        dir_name = ""
        if self.params["ui"].comboBox.currentIndex() > 0:
            self.params["ui"].comboBox.setCurrentIndex(0)
            self.params["ui"].comboBox.setCurrentText('PREVIEW')
        if self.params["ui"].dir_txt.displayText():
            dir_name = self.params["ui"].dir_txt.displayText()
            self.params["path"] = dir_name
        if os.path.exists(self.params["path"]):
            self.rename.list_files(**self.params)
        else:
            self.open_dir()

    def keep_id(self):
        index = self.params["ui"].comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def keep_ext(self):
        index = self.params["ui"].comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def search_replace(self):
        self.params["title"] = "Search & Replace"
        if len(self.params["ui"].search.displayText()):
            self.rename.search_replace(**self.params)

    def find(self):
        self.params["title"] = "Search & Replace"
        if self.params["title"] != self.params["ui"].comboBox.currentText():
            self.params["ui"].comboBox.setCurrentIndex(0)
            self.params["ui"].comboBox.setCurrentText('PREVIEW')
        if len(self.params["ui"].search.displayText()):
            self.rename.search_replace(**self.params)
        else:
            self.params["ui"].search.setFocus()

    def regex(self):
        self.search_replace()

    def index_changed(self, index):
        self.params["title"] = ""
        logging.info('self.params["path"]: %s', self.params["path"])

        # Track lower or title case change
        if index == 7 or index == 8:
            self.case_change = True
        else:
            self.case_change = False

        if index >= 1 and len(self.rename.files.filelist):
            self.params["ui"].dir_output.clear()
            self.params["title"] = self.params["ui"].comboBox.currentText()
            if index == 1:
                self.rename.remove_chars(**self.params)
            elif index == 2:
                self.rename.remove_accents(**self.params)
            elif index == 3:
                self.rename.trim_spaces(**self.params)
            elif index == 4:
                self.rename.replace_spaces(**self.params)
            elif index == 5:
                self.rename.replace_dots(**self.params)
            elif index == 6:
                self.rename.replace_hyphens(**self.params)
            elif index == 7:
                self.rename.lower_case(**self.params)
            elif index == 8:
                self.rename.title_case(**self.params)
            elif index == 9:
                self.rename.remove_ids(**self.params)
        elif index >= 1 and len(self.rename.files.filelist) == 0:
            self.open_dir()
            self.params["title"] = self.params["ui"].comboBox.currentText()
            if len(self.rename.files.filelist):
                if index == 1:
                    self.rename.remove_chars(**self.params)
                elif index == 2:
                    self.rename.remove_accents(**self.params)
                elif index == 3:
                    self.rename.trim_spaces(**self.params)
                elif index == 4:
                    self.rename.replace_spaces(**self.params)
                elif index == 5:
                    self.rename.replace_dots(**self.params)
                elif index == 6:
                    self.rename.replace_hyphens(**self.params)
                elif index == 7:
                    self.rename.lower_case(**self.params)
                elif index == 8:
                    self.rename.title_case(**self.params)
                elif index == 9:
                    self.rename.remove_ids(**self.params)

    def clear(self):
        self.params["ui"].dir_output.clear()
        self.params["ui"].rename_btn.setEnabled(False)

    def rename_files(self):
        self.params["title"] = ""
        index = self.params["ui"].comboBox.currentIndex()
        if index == 0:
            self.params["title"] = "Search & Replace"
        else:
            self.params["title"] = self.params["ui"].comboBox.currentText()
        self.rename.rename_files(**self.params)
