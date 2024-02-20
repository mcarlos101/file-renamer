# This Python file uses the following encoding: utf-8
import sys, os, logging
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from pathlib import Path

from rename import Rename
from lib.exceptions import AppError

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
# from ui_form import Ui_Widget
from ui_form import Ui_Widget


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Logs
        self.logfile = os.path.expanduser('~') + "/rename.log"
        logging.basicConfig(filename=self.logfile, filemode='w',
                            level=logging.INFO)
        logging.info("Widget __init__")

        # UI
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.path = ""

        # Create rename
        self.rename = Rename("rename", self.ui)

        self.app_error = AppError()

    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.path = Path(dir_name)
            self.ui.dir_txt.setText(str(self.path))
            self.rename.list_files(self.path, self.ui, widget)

    def add_recursively(self):
        dir_name = ""
        if self.ui.dir_txt.displayText():
            dir_name = self.ui.dir_txt.displayText()
            self.path = Path(dir_name)
        if os.path.exists(self.path):
            self.rename.list_files(self.path, self.ui, widget)
        else:
            self.open_dir()

    def keep_id(self):
        index = self.ui.comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def keep_ext(self):
        index = self.ui.comboBox.currentIndex()
        if index == 0:
            self.search_replace()
        else:
            self.index_changed(index)

    def search_replace(self):
        title = "Search & Replace"
        if len(self.ui.search.displayText()):
            self.rename.search_replace(self.path, self.ui, widget, title)

    def find(self):
        title = "Search & Replace"
        if len(self.ui.search.displayText()):
            self.rename.search_replace(self.path, self.ui, widget, title)
        else:
            self.ui.search.setFocus()

    def regex(self):
        self.search_replace()

    def index_changed(self, index):
        title = ""
        if index >= 1 and len(self.rename.files.filelist):
            self.ui.dir_output.clear()
            title = self.ui.comboBox.currentText()
            if index == 1:
                self.rename.remove_chars(self.path, self.ui, widget, title)
            elif index == 2:
                self.rename.remove_accents(self.path, self.ui, widget, title)
            elif index == 3:
                self.rename.trim_spaces(self.path, self.ui, widget, title)
            elif index == 4:
                self.rename.replace_spaces(self.path, self.ui, widget, title)
            elif index == 5:
                self.rename.replace_dots(self.path, self.ui, widget, title)
            elif index == 6:
                self.rename.replace_hyphens(self.path, self.ui, widget, title)
            elif index == 7:
                self.rename.lower_case(self.path, self.ui, widget, title)
            elif index == 8:
                self.rename.title_case(self.path, self.ui, widget, title)
            elif index == 9:
                self.rename.remove_ids(self.path, self.ui, widget, title)
        elif index >= 1 and len(self.rename.files.filelist) == 0:
            self.open_dir()
            title = self.ui.comboBox.currentText()
            if len(self.rename.files.filelist):
                if index == 1:
                    self.rename.remove_chars(self.path, self.ui, widget, title)
                elif index == 2:
                    self.rename.remove_accents(self.path, self.ui, widget, title)
                elif index == 3:
                    self.rename.trim_spaces(self.path, self.ui, widget, title)
                elif index == 4:
                    self.rename.replace_spaces(self.path, self.ui, widget, title)
                elif index == 5:
                    self.rename.replace_dots(self.path, self.ui, widget, title)
                elif index == 6:
                    self.rename.replace_hyphens(self.path, self.ui, widget, title)
                elif index == 7:
                    self.rename.lower_case(self.path, self.ui, widget, title)
                elif index == 8:
                    self.rename.title_case(self.path, self.ui, widget, title)
                elif index == 9:
                    self.rename.remove_ids(self.path, self.ui, widget, title)

    def rename_files(self):
        title = ""
        index = self.ui.comboBox.currentIndex()
        if index == 0:
            title = "Search & Replace"
        else:
            title = self.ui.comboBox.currentText()
        self.rename.rename_files(self.path, self.ui, widget, title)


if __name__ == "__main__":
    # Create widget
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    # Open the qss styles file and read in the CSS-alike styling code
    filename = Path("style/default.qss")
    with open(filename, 'r') as f:
        style = f.read()
        # Set the stylesheet of the application
        app.setStyleSheet(style)

    sys.exit(app.exec())
