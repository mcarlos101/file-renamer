import sys
import os
import re
import logging
from pathlib import Path
import os.path
from abc import ABC, abstractmethod
from PySide6.QtCore import Slot, QDir, QUrl, QFile
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QTextEdit, QToolBar, QApplication)
from PySide6.QtWebEngineWidgets import QWebEngineView
from file_renamer.lib.exceptions import AppError
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

    def __init__(self, **params):
        self.name = "WebUI"
        self.params = params
        logging.info(Path('lib/html.py'))
        logging.info('%s%s()', self.params['tab'], self.name)
        logging.info('%sself.params: %s', self.params['tab'], self.params)

        self.html_top = self.top()
        self.html_body = self.params['html_body'].strip()
        self.html_bottom = self.bottom()
        self.html_page = self.html_top + self.html_body + self.html_bottom

    def top(self):
        logging.info('%s%s.top()', self.params['tab'], self.name)
        html_top = """<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>""" + self.params['html_title'] + """</title>
        <link href='qrc:/css/bootstrap.min.css' rel="stylesheet">
        <script src='qrc:/js/bootstrap.bundle.min.js'></script>
    </head>
    <body>"""
        return html_top

    def bottom(self):
        logging.info('%s%s.bottom()', self.params['tab'], self.name)
        html_bottom = """
    </body>
</html>"""
        return html_bottom

    def validate(self, value):
        logging.info("validate")
