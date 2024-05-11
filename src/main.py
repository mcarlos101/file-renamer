import sys
import os
import logging
import platform
from pathlib import Path
from PySide6.QtCore import Slot, QFile, QIODevice, QTextStream
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTextEdit, QToolBar)
from widget import Widget
import toml
import versioningit


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)
        self.menu()

        self.dir_output = QTextEdit()

        self.params = dict(
            platform="", app=None, widget=None, ui=None, style="", path="",
            base="", dir="", name="", ext="", id="", new="", current="",
            logs=""
        )
        self.params["platform"] = platform.system()
        self.params["logs"] = os.path.expanduser('~') + "/file-renamer.log"

        self.toml = toml.load("./pyproject.toml")
        self.title = self.toml['project']['title']
        self.version = versioningit.get_version(".",)

        # Create widget
        self.widget = Widget(**self.params)
        self.widget.show()
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.title)

        if platform == "Windows":
            self.params["style"] = Path("style/default_win.qss")
        elif platform == "Darwin":
            self.params["style"] = Path("style/default_macos.qss")
        else:
            self.params["style"] = Path("style/default.qss")

        logging.info('platform: %s', self.params["platform"])
        logging.info('filename: %s', self.params["style"])

    def menu(self):
        app_menu = self.menuBar().addMenu("&App")
        icon = QIcon.fromTheme("application-exit")
        app_action = QAction(icon, "&Load", self,
                             triggered=self.show_widget)
        app_menu.addAction(app_action)
        version_action = QAction(icon, "&Version", self,
                                 triggered=self.show_version)
        app_menu.addAction(version_action)
        exit_action = QAction(icon, "&Exit", self,
                              shortcut="Ctrl+Q", triggered=self.close)
        app_menu.addAction(exit_action)

        license_menu = self.menuBar().addMenu("&License")
        license_action = QAction(icon, "GPL", self,
                                 triggered=self.show_license)
        license_menu.addAction(license_action)

        qt_python_menu = self.menuBar().addMenu("&Qt for Python")
        qt_python_action = QAction(icon, "PySide", self,
                                   triggered=self.show_qt_for_python)
        qt_python_menu.addAction(qt_python_action)

    def show_widget(self):
        if not self.dir_output:
            self.dir_output.hide()
        self.widget = Widget(**self.params)
        self.widget.show()
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.title)

    def show_output(self):
        if not self.widget:
            self.widget.hide()
        self.dir_output = QTextEdit()
        self.dir_output.setObjectName(u"dir_output")
        self.dir_output.setReadOnly(True)
        self.setCentralWidget(self.dir_output)

    def open_file(self, file, title, append=False):
        stream = QTextStream(file)
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            while not file.atEnd():
                text = stream.readAll()
                if append:
                    self.dir_output.append(str(text))
                else:
                    self.dir_output.setText(str(text))
                self.dir_output.show()
                self.dir_output.setFocus()
                self.setWindowTitle(title)

    @Slot()
    def show_version(self):
        self.show_output()
        self.dir_output.clear()
        self.dir_output.append(self.title + ' ' + self.version)
        self.dir_output.append("")
        file = QFile("docs/Version.txt")
        title = "Version"
        append = True
        self.open_file(file, title, append)

    @Slot()
    def show_license(self):
        self.show_output()
        self.dir_output.clear()
        file = QFile("docs/License.txt")
        title = "License"
        append = False
        self.open_file(file, title, append)

    @Slot()
    def show_qt_for_python(self, data):
        self.show_output()
        self.dir_output.clear()
        file = QFile("docs/Qt-for-Python.txt")
        title = "Qt for Python"
        append = False
        self.open_file(file, title, append)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()
