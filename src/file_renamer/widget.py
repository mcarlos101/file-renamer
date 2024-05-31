# This Python file uses the following encoding: utf-8
import sys
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
    def __init__(self, parent=None, **fr):
        super().__init__(parent)
        self.name = 'Widget'
        self.fr = fr
        logging.info('widget.py')
        logging.info('%s%s()', self.fr['tab'], self.name)
        logging.info('%sself.fr: %s', self.fr['tab'], self.fr)

        # UI
        self.fr["ui"] = Ui_Widget()
        self.fr["ui"].setupUi(self)

        # Create rename
        self.rename = Rename(**self.fr)

        self.app_error = AppError()

        # Track lower or title case change
        self.fr["case_change"] = False

    def open_dir(self):
        logging.info('%s%s.open_dir()', self.fr['tab'], self.name)
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.fr["path"] = Path(dir_name)
            self.fr["ui"].dir_txt.setText(str(self.fr["path"]))
            self.rename.list_files(**self.fr)

    def add_recursively(self):
        logging.info('%s%s.add_recursively()', self.fr['tab'], self.name)
        dir_name = ""
        if self.fr["ui"].comboBox.currentIndex() > 0:
            self.fr["ui"].comboBox.setCurrentIndex(0)
            self.fr["ui"].comboBox.setCurrentText('PREVIEW')
        if self.fr["ui"].dir_txt.displayText():
            dir_name = self.fr["ui"].dir_txt.displayText()
            self.fr["path"] = dir_name
        if os.path.exists(self.fr["path"]):
            self.rename.list_files(**self.fr)
        else:
            self.open_dir()

    def keep_id(self):
        logging.info('%s%s.keep_id()', self.fr['tab'], self.name)
        index = self.fr["ui"].comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def keep_ext(self):
        logging.info('%s%s.keep_ext()', self.fr['tab'], self.name)
        index = self.fr["ui"].comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def search_replace(self):
        logging.info('%s%s.search_replace()', self.fr['tab'], self.name)
        self.fr["title"] = "Search & Replace"
        if len(self.fr["ui"].search.displayText()):
            self.rename.search_replace(**self.fr)

    def find(self):
        logging.info('%s%s.find()', self.fr['tab'], self.name)
        self.fr["title"] = "Search & Replace"
        if self.fr["title"] != self.fr["ui"].comboBox.currentText():
            self.fr["ui"].comboBox.setCurrentIndex(0)
            self.fr["ui"].comboBox.setCurrentText('PREVIEW')
        if len(self.fr["ui"].search.displayText()):
            self.rename.search_replace(**self.fr)
        else:
            self.fr["ui"].search.setFocus()

    def regex(self):
        logging.info('%s%s.regex()', self.fr['tab'], self.name)
        self.search_replace()

    def index_changed(self, index):
        logging.info('%s%s.index_changed()', self.fr['tab'], self.name)
        self.fr["title"] = ""
        logging.info(
            '%sself.fr["path"]: %s',
            self.fr['tab'],
            self.fr["path"]
        )

        # Track lower or title case change
        if index == 7 or index == 8:
            self.case_change = True
        else:
            self.case_change = False

        if index >= 1 and len(self.rename.files.filelist):
            self.fr["ui"].dir_output.clear()
            self.fr["title"] = self.fr["ui"].comboBox.currentText()
            if index == 1:
                self.rename.remove_chars(**self.fr)
            elif index == 2:
                self.rename.remove_accents(**self.fr)
            elif index == 3:
                self.rename.trim_spaces(**self.fr)
            elif index == 4:
                self.rename.replace_spaces(**self.fr)
            elif index == 5:
                self.rename.replace_dots(**self.fr)
            elif index == 6:
                self.rename.replace_hyphens(**self.fr)
            elif index == 7:
                self.rename.lower_case(**self.fr)
            elif index == 8:
                self.rename.title_case(**self.fr)
            elif index == 9:
                self.rename.remove_ids(**self.fr)
        elif index >= 1 and len(self.rename.files.filelist) == 0:
            self.open_dir()
            self.fr["title"] = self.fr["ui"].comboBox.currentText()
            if len(self.rename.files.filelist):
                if index == 1:
                    self.rename.remove_chars(**self.fr)
                elif index == 2:
                    self.rename.remove_accents(**self.fr)
                elif index == 3:
                    self.rename.trim_spaces(**self.fr)
                elif index == 4:
                    self.rename.replace_spaces(**self.fr)
                elif index == 5:
                    self.rename.replace_dots(**self.fr)
                elif index == 6:
                    self.rename.replace_hyphens(**self.fr)
                elif index == 7:
                    self.rename.lower_case(**self.fr)
                elif index == 8:
                    self.rename.title_case(**self.fr)
                elif index == 9:
                    self.rename.remove_ids(**self.fr)

    def clear(self):
        logging.info('%s%s.clear()', self.fr['tab'], self.name)
        self.fr["ui"].dir_output.clear()
        self.fr["ui"].rename_btn.setEnabled(False)

    def rename_files(self):
        logging.info('%s%s.rename_files()', self.fr['tab'], self.name)
        self.fr["title"] = ""
        index = self.fr["ui"].comboBox.currentIndex()
        if index == 0:
            self.fr["title"] = "Search & Replace"
        else:
            self.fr["title"] = self.fr["ui"].comboBox.currentText()
        self.rename.rename_files(**self.fr)
