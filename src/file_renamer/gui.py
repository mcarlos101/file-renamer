import logging
logger = logging.getLogger(__name__)
import inspect
import PySide6.QtCore
from PySide6.QtCore import (Slot, QDir)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QTextEdit, QToolBar
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from file_renamer.widget import Widget
from file_renamer.lib.html import WebUI


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget = None, **fr):
        super().__init__(parent)
        self.fr = fr
        self.title = "File Renamer"
        self.qdir = QDir()
        self.dir_output = QTextEdit()

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)
        self.menu()

        # Create widget
        self.widget = Widget(**self.fr)
        self.widget.show()
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.title)
        self.fr['page-id'] = 'app'

    def menu(self):
        app_icon = QIcon.fromTheme("application-x-executable")
        html_icon = QIcon.fromTheme("text-html")
        exit_icon = QIcon.fromTheme("application-exit")
        video_icon = QIcon.fromTheme("video-x-generic")

        app_menu = self.menuBar().addMenu("&App")
        app_action = QAction(
            app_icon, "&Load", self, triggered=self.show_widget
        )
        app_menu.addAction(app_action)
        version_action = QAction(
            html_icon, "&Version", self, triggered=self.show_version
        )
        app_menu.addAction(version_action)
        exit_action = QAction(
            exit_icon, "&Exit", self, shortcut="Ctrl+Q",
            triggered=self.close
        )
        app_menu.addAction(exit_action)

        theme_menu = self.menuBar().addMenu("&Theme")
        dark_theme_action = QAction(
            html_icon, 'Dark', self, triggered=self.set_dark_theme
        )
        theme_menu.addAction(dark_theme_action)

        light_theme_action = QAction(
            html_icon, 'Light', self, triggered=self.set_light_theme
        )
        theme_menu.addAction(light_theme_action)

        license_menu = self.menuBar().addMenu("&License")
        license_action = QAction(
            html_icon, "GPL", self, triggered=self.show_license
        )
        license_menu.addAction(license_action)

        qt_python_menu = self.menuBar().addMenu("&Qt for Python")
        qt_python_action = QAction(
            html_icon, "PySide6", self, triggered=self.show_qt_for_python
        )
        qt_python_menu.addAction(qt_python_action)

    def show_widget(self):
        if self.fr['page-id'] != 'app':
            if not self.dir_output:
                self.dir_output.hide()
            self.widget = Widget(**self.fr)
            self.widget.show()
            self.setCentralWidget(self.widget)
            self.setWindowTitle(self.title)
            self.fr['page-id'] = 'app'

    def render_html(self):
        qweb = QWebEngineView()
        webui = WebUI(**self.fr)
        html = webui.html_page.strip()
        qweb.setHtml(html)
        self.setCentralWidget(qweb)
        self.setWindowTitle(self.fr['html_title'])

    @Slot()
    def show_version(self):
        if self.fr['page-id'] != 'version':
            from file_renamer.__version__ import __version__
            title = "Version"
            body = """
            <div class="container">
                <h1>File Renamer """ + __version__ + """</h1>
                <p>GitHub<br>
                    https://github.com/mcarlos101/file-renamer/
                </p>
                <p>Python Package Index<br>
                    https://pypi.org/project/file-renamer/
                </p>
                <p>Flathub (Coming Soon)<br>
                    https://flathub.org/apps/io.github.mcarlos101.file-renamer
                </p>
            </div>"""
            self.fr['html_title'] = title
            self.fr['html_body'] = body
            self.fr['page-id'] = 'version'
            self.render_html()

    def set_theme(self):
        qss = ""
        if self.fr["platform"] == "Windows":
            if self.fr['theme'] == 'light':
                from file_renamer.themes.light.light_windows import (
                    LightWindows
                )
                style = LightWindows()
                qss = style.theme
            elif self.fr['theme'] == 'dark':
                from file_renamer.themes.dark.dark_windows import DarkWindows
                style = DarkWindows()
                qss = style.theme
        else:
            if self.fr['theme'] == 'light':
                from file_renamer.themes.light.light_linux import LightLinux
                style = LightLinux()
                qss = style.theme
            elif self.fr['theme'] == 'dark':
                from file_renamer.themes.dark.dark_linux import DarkLinux
                style = DarkLinux()
                qss = style.theme
        if qss:
            self.fr['app'].setStyleSheet(qss)
            if self.fr['page-id'] == 'version':
                self.fr['page-id'] = ""
                self.show_version()
            elif self.fr['page-id'] == 'license':
                self.fr['page-id'] = ""
                self.show_license()
            elif self.fr['page-id'] == 'qt-python':
                self.fr['page-id'] = ""
                self.show_qt_for_python()
            elif self.fr['page-id'] == 'peace':
                self.fr['page-id'] = ""
                self.show_peace()
            elif self.fr['page-id'] == 'rbe':
                self.fr['page-id'] = ""
                self.show_rbe()
        else:
            logger.info('theme NOT set: %s', self.fr['theme'])

    @Slot()
    def set_dark_theme(self):
        if self.fr['theme'] != 'dark':
            self.fr['theme'] = 'dark'
            self.set_theme()

    @Slot()
    def set_light_theme(self):
        if self.fr['theme'] != 'light':
            self.fr['theme'] = 'light'
            self.set_theme()

    @Slot()
    def show_license(self):
        if self.fr['page-id'] != 'license':
            title = "License"
            body = """
            <div class="container">
                <h1>Copyright (C) 2024  Carlos</h1>

                <p>This program is free software: you can redistribute it
                and/or modify it under the terms of the GNU General Public
                License as published by the Free Software Foundation, either
                version 3 of the License, or (at your option) any later
                version.</p>

                <p>This program is distributed in the hope that it will be
                useful, but WITHOUT ANY WARRANTY; without even the implied
                warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
                PURPOSE.  See the GNU General Public License for more
                details.</p>

                <p>You should have received a copy of the GNU General Public
                License along with this program.  If not, see
                https://www.gnu.org/licenses/.</p>
            </div>"""
            self.fr['html_title'] = title
            self.fr['html_body'] = body
            self.fr['page-id'] = 'license'
            self.render_html()

    @Slot()
    def show_qt_for_python(self):
        if self.fr['page-id'] != 'qt-python':
            title = "Qt for Python"
            body = """
            <div class="container">
                <h1>Qt for Python</h1>

                <div class="p-3 text-primary-emphasis bg-primary-subtle \
                    border border-primary-subtle rounded-3">
                    Versions
                    <ul>
                        <li>
                            <strong>Qt</strong>:&nbsp;&nbsp;""" \
                            + PySide6.QtCore.__version__ + """
                        </li>
                        <li><strong>PySide6</strong>:&nbsp;&nbsp;""" \
                            + PySide6.__version__ + """
                        </li>
                    </ul>
                </div>

                <p>Qt for Python offers the official Python bindings for Qt,
                which enables you to use Python to write your Qt applications.
                The project has two main components:</p>
                    <ol>
                        <li>PySide6, so that you can use Qt6 APIs in your
                            Python applications, and</li>

                        <li>Shiboken6, a binding generator tool, which can be
                            used to expose C++ projects to Python, and a Python
                            module with some utility functions.</li>
                    </ol>
                <p>This project is available under the LGPLv3/GPLv3 and the Qt
                commercial license.</p>

                <p>Qt for Python<br>
                https://www.qt.io/qt-for-python</p>

                <p>Docs<br>
                https://doc.qt.io/qtforpython-6/</p>
            </div>"""
            self.fr['html_title'] = title
            self.fr['html_body'] = body
            self.fr['page-id'] = 'qt-python'
            self.render_html()
