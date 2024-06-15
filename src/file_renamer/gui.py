import logging
import inspect
import PySide6.QtCore
from PySide6.QtCore import (Slot, QDir, QFile, QIODevice,
                            QTextStream)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QTextEdit, QToolBar)
from PySide6.QtWebEngineWidgets import QWebEngineView
from file_renamer.widget import Widget
from file_renamer.lib.html import WebUI
from file_renamer.lib.exceptions import Messages


class MainWindow(QMainWindow):

    def __init__(self, parent: QWidget = None, **fr):
        super().__init__(parent)

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.fr = fr
        logging.info('fr: %s', fr)

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
        logging.info(inspect.stack()[0].function)  # method name

        # Linux icons
        app_icon = QIcon.fromTheme("application-x-executable")
        # app_icon = QIcon('icons/file-renamer-32x32.png')
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

        imagine_menu = self.menuBar().addMenu("&Imagine")
        peace_action = QAction(
            video_icon, "Peace on Earth", self, triggered=self.show_peace
        )
        imagine_menu.addAction(peace_action)

        rbe_action = QAction(
            video_icon, "Resource Based Economy", self,
            triggered=self.show_rbe
        )
        imagine_menu.addAction(rbe_action)

    def show_widget(self):
        logging.info(inspect.stack()[0].function)  # method name
        if not self.dir_output:
            self.dir_output.hide()
        self.widget = Widget(**self.fr)
        self.widget.show()
        self.setCentralWidget(self.widget)
        self.setWindowTitle(self.title)
        self.fr['page-id'] = 'app'

    def render_html(self):
        logging.info(inspect.stack()[0].function)  # method name
        qweb = QWebEngineView()
        webui = WebUI(**self.fr)
        logging.info("self.fr: %s", self.fr)
        html = webui.html_page.strip()
        logging.info("html: %s", html)
        logging.info('set html')
        qweb.setHtml(html)
        self.setCentralWidget(qweb)
        self.setWindowTitle(self.fr['html_title'])

    @Slot()
    def show_version(self):
        logging.info(inspect.stack()[0].function)  # method name
        from file_renamer.version import __version__
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
        </div>"""
        self.fr['html_title'] = title
        self.fr['html_body'] = body
        self.fr['page-id'] = 'show_version'
        self.render_html()

    def set_theme(self):
        logging.info(inspect.stack()[0].function)  # method name

        logging.info('self.fr["theme"]: %s', self.fr["theme"])
        qss = ""
        logging.info('self.fr["platform"]: %s', self.fr["platform"])
        if self.fr["platform"] == "Windows":
            if self.fr['theme'] == 'light':
                from file_renamer.themes.light.light_windows import (
                    LightWindows
                )
                style = LightWindows()
                qss = style.theme
                logging.info('qss: %s', qss)
            elif self.fr['theme'] == 'dark':
                from file_renamer.themes.dark.dark_windows import DarkWindows
                style = DarkWindows()
                qss = style.theme
                logging.info('qss: %s', qss)
        else:
            if self.fr['theme'] == 'light':
                from file_renamer.themes.light.light_linux import LightLinux
                style = LightLinux()
                qss = style.theme
                logging.info('qss: %s', qss)
            elif self.fr['theme'] == 'dark':
                from file_renamer.themes.dark.dark_linux import DarkLinux
                style = DarkLinux()
                qss = style.theme
                logging.info('qss: %s', qss)
        if qss:
            self.fr['app'].setStyleSheet(qss)
            logging.info('theme set: %s', self.fr['theme'])
            if self.fr['page-id'] == 'show_version':
                self.show_version()
            elif self.fr['page-id'] == 'show_license':
                self.show_license()
            elif self.fr['page-id'] == 'show_qt_for_python':
                self.show_qt_for_python()
            elif self.fr['page-id'] == 'show_peace':
                self.show_peace()
            elif self.fr['page-id'] == 'show_rbe':
                self.show_rbe()

        else:
            logging.info('theme NOT set: %s', self.fr['theme'])

    @Slot()
    def set_dark_theme(self):
        logging.info(inspect.stack()[0].function)  # method name
        logging.info('self.fr["theme"]: %s', self.fr["theme"])
        if self.fr['theme'] != 'dark':
            self.fr['theme'] = 'dark'
            logging.info('self.fr["theme"]: %s', self.fr["theme"])
            self.set_theme()

    @Slot()
    def set_light_theme(self):
        logging.info(inspect.stack()[0].function)  # method name
        logging.info('self.fr["theme"]: %s', self.fr["theme"])
        if self.fr['theme'] != 'light':
            self.fr['theme'] = 'light'
            logging.info('self.fr["theme"]: %s', self.fr["theme"])
            self.set_theme()

    @Slot()
    def show_license(self):
        logging.info(inspect.stack()[0].function)  # method name
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
        self.fr['html_title'] = title
        self.fr['html_body'] = body
        self.fr['page-id'] = 'show_license'
        self.render_html()

    @Slot()
    def show_qt_for_python(self):
        logging.info(inspect.stack()[0].function)  # method name
        title = "Qt for Python"
        body = """
        <div class="container">
            <h1>Qt for Python</h1>

            <div class="p-3 text-primary-emphasis bg-primary-subtle border \
                border-primary-subtle rounded-3">
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
        self.fr['html_title'] = title
        self.fr['html_body'] = body
        self.fr['page-id'] = 'show_qt_for_python'
        self.render_html()

    @Slot()
    def show_peace(self):
        logging.info(inspect.stack()[0].function)  # method name
        import file_renamer.html.rc_imagine
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
        self.fr['html_title'] = title
        self.fr['html_body'] = body
        self.fr['page-id'] = 'show_peace'
        self.render_html()

    @Slot()
    def show_rbe(self):
        logging.info(inspect.stack()[0].function)  # method name
        import file_renamer.html.rc_rbe
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
        self.fr['html_title'] = title
        self.fr['html_body'] = body
        self.fr['page-id'] = 'show_rbe'
        self.render_html()
