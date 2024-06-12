import sys
import os
import re
import logging
import os.path
import inspect
from pathlib import Path
from abc import ABC, abstractmethod
from PySide6.QtCore import Slot, QDir, QUrl, QFile
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QTextEdit, QToolBar, QApplication)
from PySide6.QtWebEngineWidgets import QWebEngineView
from file_renamer.lib.exceptions import Messages
from file_renamer.lib.case_insensitive import CaseInsensitive
import file_renamer.html.rc_ui


class UI(ABC):

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


class WebUI(UI):

    def __init__(self, **fr):

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.fr = fr
        logging.info('fr: %s', fr)

        self.html_top = self.top()
        self.html_body = self.fr['html_body'].strip()
        self.html_bottom = self.bottom()
        self.html_page = self.html_top + self.html_body + self.html_bottom

    def top(self):
        logging.info(inspect.stack()[0].function)  # method name
        html_top = """<!doctype html>
<html lang="en" data-bs-theme='""" + self.fr['theme'] + """'>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>""" + self.fr['html_title'] + """</title>
        <link href='qrc:/css/bootstrap.min.css' rel="stylesheet">
    </head>
    <body>"""
        return html_top

    def bottom(self):
        logging.info(inspect.stack()[0].function)  # method name
        html_bottom = """
    <script src='qrc:/js/bootstrap.bundle.min.js'></script>
    </body>
</html>"""
        return html_bottom

    def validate(self, value):
        logging.info(inspect.stack()[0].function)  # method name
        logging.info("validate")
