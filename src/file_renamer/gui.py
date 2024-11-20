import logging
logger = logging.getLogger(__name__)
import sys
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

        about_menu = self.menuBar().addMenu("&About")
        python_action = QAction(
            html_icon, 'Python3', self, triggered=self.show_python
        )
        about_menu.addAction(python_action)
        pyside_action = QAction(
            html_icon, 'PySide6', self, triggered=self.show_pyside
        )
        about_menu.addAction(pyside_action)
        bootstrap_action = QAction(
            html_icon, 'Bootstrap', self, triggered=self.show_bootstrap
        )
        about_menu.addAction(bootstrap_action)

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
                <p><strong>GitHub</strong><br>
                    https://github.com/mcarlos101/file-renamer/
                </p>
                <p><strong>Python Package Index</strong><br>
                    https://pypi.org/project/file-renamer/
                </p>
                <p><strong>Flathub (Coming Soon)</strong><br>
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
            elif self.fr['page-id'] == 'python':
                self.fr['page-id'] = ""
                self.show_python()
            elif self.fr['page-id'] == 'pyside':
                self.fr['page-id'] = ""
                self.show_pyside()
            elif self.fr['page-id'] == 'bootstrap':
                self.fr['page-id'] = ""
                self.show_bootstrap()
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
                and/or modify it under the terms of the <strong>GNU General
                Public License</strong> as published by the Free Software
                Foundation, either version 3 of the License, or (at your option)
                any later version.</p>

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
    def show_python(self):
        if self.fr['page-id'] != 'python':
            title = "Python"
            version = sys.version
            body = """
            <div class="container">
                <h1>Python</h1>

                <div class="p-3 text-primary-emphasis bg-primary-subtle \
                    border border-primary-subtle rounded-3">
                    Version
                    <ul>
                        <li>
                            <strong>Python</strong>&nbsp;&nbsp;""" \
                            + version + """
                        </li>
                    </ul>
                </div>

                <p>Python is an interpreted, interactive, object-oriented programming language.</p>

                <p><strong>Python</strong><br>
                https://www.python.org</p>

                <p><strong>Docs</strong><br>
                https://docs.python.org</p>
            </div>"""
            self.fr['html_title'] = title
            self.fr['html_body'] = body
            self.fr['page-id'] = 'python'
            self.render_html()

    @Slot()
    def show_pyside(self):
        if self.fr['page-id'] != 'pyside':
            title = "Qt for Python"
            body = """
            <div class="container">
                <h1>Qt for Python</h1>

                <div class="p-3 text-primary-emphasis bg-primary-subtle \
                    border border-primary-subtle rounded-3">
                    Versions
                    <ul>
                        <li>
                            <strong>Qt</strong>&nbsp;&nbsp;""" \
                            + PySide6.QtCore.__version__ + """
                        </li>
                        <li><strong>PySide6</strong>&nbsp;&nbsp;""" \
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

                <p><strong>Qt for Python</strong><br>
                https://www.qt.io/qt-for-python</p>

                <p><strong>Docs</strong><br>
                https://doc.qt.io/qtforpython-6</p>
            </div>"""
            self.fr['html_title'] = title
            self.fr['html_body'] = body
            self.fr['page-id'] = 'pyside'
            self.render_html()

    @Slot()
    def show_bootstrap(self):
        if self.fr['page-id'] != 'bootstrap':
            title = "Bootstrap"
            version = "5.3.3"
            body = """
            <div class="container">
                <h1>Bootstrap</h1>

                <div class="p-3 text-primary-emphasis bg-primary-subtle \
                    border border-primary-subtle rounded-3">
                    Version
                    <ul>
                        <li>
                            <strong>Bootstrap</strong>&nbsp;&nbsp;""" \
                            + version + """
                        </li>
                    </ul>
                </div>

                <p>Bootstrap is a powerful, feature-packed frontend toolkit.</p>

                <p><strong>Bootstrap</strong><br>
                https://getbootstrap.com</p>

                <p><strong>Docs</strong><br>
                https://getbootstrap.com</p>
            </div>"""
            self.fr['html_title'] = title
            self.fr['html_body'] = body
            self.fr['page-id'] = 'bootstrap'
            self.render_html()
