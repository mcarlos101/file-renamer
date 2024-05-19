import sys
import os
import logging
import platform
from pathlib import Path
from PySide6 import QtCore
from PySide6.QtCore import Slot, QFile, QDir
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QTextEdit, QToolBar)
from PySide6.QtWebEngineWidgets import QWebEngineView
from file_renamer.widget import Widget


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.title = "File Renamer"
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

        # Create widget
        self.widget = Widget(**self.params)
        self.widget.show()
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.title)

        self.qdir = QDir()

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

    def open_file(self, title, filename):
        error = "ERROR"
        qweb = QWebEngineView()
        qfile = self.qdir.currentPath() + filename

        try:
            if QFile.exists(qfile):
                qweb.load(QtCore.QUrl("file:///" + qfile))
            else:
                error = "File Not Found: " + qfile
                raise FileNotFoundError()
        except FileNotFoundError:
            print('logs: ', self.params["logs"])
            logging.info('error: %s', error)
            logging.info('qfile: %s', qfile)
            logging.info('self.qdir.currentPath: %s', self.qdir.currentPath())

        else:
            self.setCentralWidget(qweb)
            self.setWindowTitle(title)

    @Slot()
    def show_version(self):
        title = "License"
        filename = "/html/version.html"
        self.open_file(title, filename)

    @Slot()
    def show_license(self):
        title = "License"
        filename = "/html/license.html"
        self.open_file(title, filename)

    @Slot()
    def show_qt_for_python(self):
        title = "Qt for Python"
        filename = "/html/qt-for-python.html"
        self.open_file(title, filename)
