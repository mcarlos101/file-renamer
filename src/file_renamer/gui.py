import sys
import os
import logging
import platform
from pathlib import Path
from PySide6.QtCore import Slot, QDir, QUrl, QFile
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QTextEdit, QToolBar, QApplication)
from PySide6.QtWebEngineWidgets import QWebEngineView
from file_renamer.widget import Widget
from file_renamer.lib.html import WebUI
import file_renamer.html.rc_imagine
import file_renamer.html.rc_rbe


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.title = "File Renamer"
        self.qdir = QDir()
        self.dir_output = QTextEdit()

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)
        self.menu()

        self.params = dict(
            platform="", app=None, widget=None, ui=None, style="", path="",
            base="", dir="", name="", ext="", id="", new="", current="",
            logs=os.path.expanduser('~') + "/file-renamer.log"
        )

        # Logs
        logging.basicConfig(
            filename=self.params["logs"],
            filemode='w',
            level=logging.INFO
        )
        self.params["platform"] = platform.system()
        logging.info('platform: %s', self.params["platform"])

        # Create widget
        self.widget = Widget(**self.params)
        self.widget.show()
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.title)

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

        imagine_menu = self.menuBar().addMenu("&Imagine")
        peace_action = QAction(icon, "Peace on Earth", self,
                               triggered=self.show_peace)
        imagine_menu.addAction(peace_action)

        rbe_action = QAction(icon, "Resource Based Economy", self,
                             triggered=self.show_rbe)
        imagine_menu.addAction(rbe_action)

    def show_widget(self):
        if not self.dir_output:
            self.dir_output.hide()
        self.widget = Widget(**self.params)
        self.widget.show()
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.title)

    def open_file(self, **html_params):
        qweb = QWebEngineView()
        webui = WebUI(**html_params)
        html = webui.html_page.strip()
        logging.info("html: %s", html)
        logging.info('set html')
        qweb.setHtml(html)
        self.setCentralWidget(qweb)
        self.setWindowTitle(html_params['title'])

    @Slot()
    def show_version(self):
        title = "Version"
        body = """
        <div class="container">
            <h1>File Renamer 1.0.6</h1>
            <p>GitHub<br>
                https://github.com/mcarlos101/file-renamer/
            </p>
            <p>Python Package Index<br>
                https://pypi.org/project/file-renamer/
            </p>
        </div>"""
        html_params = dict(
            title=title,
            body=body
        )
        self.open_file(**html_params)

    @Slot()
    def show_license(self):
        title = "License"
        body = """
        <div class="container">
            <h1>Copyright (C) 2024  Carlos</h1>

            <p>This program is free software: you can redistribute it and/or
            modify it under the terms of the GNU General Public License as
            published by the Free Software Foundation, either version 3 of the
            License, or (at your option) any later version.</p>

            <p>This program is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU General Public License for more details.</p>

            <p>You should have received a copy of the GNU General Public
            License along with this program.  If not, see
            https://www.gnu.org/licenses/.</p>
        </div>"""
        html_params = dict(
            title=title,
            body=body
        )
        self.open_file(**html_params)

    @Slot()
    def show_qt_for_python(self):
        title = "Qt for Python"
        body = """
        <div class="container">
            <h1>Qt for Python</h1>

            <p>Qt for Python offers the official Python bindings for Qt, which
            enables you to use Python to write your Qt applications. The
            project has two main components:</p>
                <ol>
                    <li>PySide6, so that you can use Qt6 APIs in your Python
                    applications, and</li>

                    <li>Shiboken6, a binding generator tool, which can be used
                    to expose C++ projects to Python, and a Python module with
                    some utility functions.</li>
                </ol>
            <p>This project is available under the LGPLv3/GPLv3 and the Qt
            commercial license.</p>

            <p>Qt for Python<br>
            https://www.qt.io/qt-for-python</p>

            <p>Docs<br>
            https://doc.qt.io/qtforpython-6/</p>
        </div>"""
        html_params = dict(
            title=title,
            body=body
        )
        self.open_file(**html_params)

    @Slot()
    def show_peace(self):
        title = "Imagine Peace On Earth"
        body = """
        <div class="container text-center">
            <div class="row">
                <h1>""" + title + """</h1>
                <video controls autoplay>
                  <source src='qrc:/imagine_mp4' type="video/mp4" codecs="vp9">
                Your browser does not support the video tag.
                </video>
            </div>
        </div>
        <div class="container">
            <h2>Credits</h2>
            <p>
                Song: John Lennon - Imagine (1971)<br>
                Background Image: https://pngkit.com</p>
            <p>
                Copyright Disclaimer under Section 107 of the Copyright Act of
                1976: Allowance is made for "fair use" for purposes such as
                criticism, comment, news reporting, teaching, scholarship,
                education, and research.<br>
                Fair use is a use permitted by copyright statute that might
                otherwise be infringing.<br>
                All rights and credit go directly to its rightful owners. No
                copyright infringement is intended.
            </p>
        </div>
"""
        html_params = dict(
            title=title,
            body=body
        )
        self.open_file(**html_params)

    @Slot()
    def show_rbe(self):
        title = "Resource Based Economy"
        body = """
        <div class="container text-center">
            <div class="row">
                <h1>""" + title + """</h1>
                <video controls autoplay>
                  <source src='qrc:/venus_project_mp4' type="video/mp4"
                  codecs="vp9">
                Your browser does not support the video tag.
                </video>
            </div>
        </div>
        <div class="container">
            <h2>Credits</h2>
            <p>
                Song: The Lost Children Of Babylon -  The Venus Project
                (2010)<br>
                https://lostchildrenofbabylon.com/</p>
            <p>
                Background Image: https://www.resourcebasedeconomy.org
            </p>
            <p>
                Copyright Disclaimer under Section 107 of the Copyright Act of
                1976: Allowance is made for "fair use" for purposes such as
                criticism, comment, news reporting, teaching, scholarship,
                education, and research.<br>
                Fair use is a use permitted by copyright statute that might
                otherwise be infringing.<br>
                All rights and credit go directly to its rightful owners. No
                copyright infringement is intended.
            </p>
        </div>"""
        html_params = dict(
            title=title,
            body=body
        )
        self.open_file(**html_params)
