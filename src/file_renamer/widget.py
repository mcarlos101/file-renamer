import logging
logger = logging.getLogger(__name__)
import os
import inspect
from pathlib import Path
from PySide6.QtWidgets import QWidget, QFileDialog
from file_renamer.rename import Rename
from file_renamer.ui_form import Ui_Widget


class Widget(QWidget):
    def __init__(self, parent=None, **fr):
        super().__init__(parent)
        logger.info('class Widget')
        self.fr = fr
        # UI
        self.fr["ui"] = Ui_Widget()
        self.fr["ui"].setupUi(self)
        # Create rename
        self.rename = Rename(**self.fr)
        # Track lower or title case change
        self.fr["case_change"] = False

    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.fr["path"] = Path(dir_name)
            self.fr["ui"].dir_txt.setText(str(self.fr["path"]))
            self.fr["ui"].label.setText('LIST FILES')
            self.rename.list_files(**self.fr)

    def add_recursively(self):
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
            self.fr["ui"].label.setText('LIST FILES')
            self.open_dir()

    def keep_id(self):
        index = self.fr["ui"].comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def keep_ext(self):
        index = self.fr["ui"].comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def search_replace(self):
        self.fr["title"] = "Search & Replace"
        if len(self.fr["ui"].search.displayText()):
            self.rename.search_replace(**self.fr)

    def find(self):
        self.fr["title"] = "Search & Replace"
        if self.fr["title"] != self.fr["ui"].comboBox.currentText():
            self.fr["ui"].comboBox.setCurrentIndex(0)
            self.fr["ui"].comboBox.setCurrentText('PREVIEW')
        if len(self.fr["ui"].search.displayText()):
            self.rename.search_replace(**self.fr)
        else:
            self.fr["ui"].search.setFocus()

    def regex(self):
        self.search_replace()

    def index_changed(self, index):
        self.fr["title"] = ""
        logger.info('index: %s', index)
        # Track lower or title case change
        if index == 7 or index == 8:
            self.case_change = True
        else:
            self.case_change = False
        logger.info('self.case_change: %s', self.case_change)
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
            elif index == 10:
                self.rename.number(**self.fr)
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
                elif index == 10:
                    self.rename.number(**self.fr)

    def clear(self):
        self.rename.files.filelist.clear()
        self.rename.files.changed.clear()
        self.fr["ui"].rename_btn.setEnabled(False)
        self.fr["ui"].label.setText("PREVIEW")
        if self.fr['theme'] == 'light':
            self.fr["ui"].label.setStyleSheet(
                "color: white; background-color: gray;"
            )
        elif self.fr['theme'] == 'dark':
            self.fr["ui"].label.setStyleSheet(
                "color: white; background-color: black;"
            )
        self.fr["ui"].dir_output.clear()
        self.fr["ui"].search.clear()
        self.fr["ui"].replace.clear()

    def rename_files(self):
        self.fr["title"] = ""
        index = self.fr["ui"].comboBox.currentIndex()
        if index == 0:
            self.fr["title"] = "Search & Replace"
        else:
            self.fr["title"] = self.fr["ui"].comboBox.currentText()
        self.rename.rename_files(**self.fr)
