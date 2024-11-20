import logging
logger = logging.getLogger(__name__)
import sys
import os
import platform
import inspect
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir, QFile, QFileInfo, QIODevice, QTextStream
from file_renamer.gui import MainWindow
from file_renamer.__version__ import __version__


def start_app(**fr):
    # Logs
    home = os.path.expanduser('~')
    logfile = Path(home + "/file-renamer.log")
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=logfile,
        encoding='utf-8',
        filemode='w',
        level=logging.DEBUG
    )
    logger.info('File Renamer %s Logs', __version__)
    function = inspect.stack()[0].function
    logger.info(function)
    sys_platform = platform.system()
    logger.info('sys_platform: %s', sys_platform)

    # File Renamer dict
    fr = {
        "home": home,
        "logfile": logfile,
        "app": "",
        "platform": sys_platform,
        "case_sensitive": False,
        "write": False,
        "widget": None,
        "ui": None,
        "path": "",
        "base": "",
        "dir": "",
        "name": "",
        "ext": "",
        "id": "",
        "new": "",
        "current": "",
        "html_title": "",
        "html_body": "",
        "page-id": "app",
        "theme": 'light',
        "msg-type": "info",
        "msg-title": "MESSAGE",
        "msg-info": "Unknown"
    }

    # File Renamer app
    app = QApplication(sys.argv)
    fr['app'] = app

    # Default screen resolution
    width = 800
    height = 600

    window = MainWindow(**fr)
    window.resize(width, height)
    window.show()

    # Set theme
    qss = ""
    if fr["platform"] == "Windows":
        if fr['theme'] == 'light':
            from file_renamer.themes.light.light_windows import (
                LightWindows
            )
            style = LightWindows()
            qss = style.theme
        elif fr['theme'] == 'dark':
            from file_renamer.themes.dark.dark_windows import DarkWindows
            style = DarkWindows()
            qss = style.theme
    else:
        if fr['theme'] == 'light':
            from file_renamer.themes.light.light_linux import LightLinux
            style = LightLinux()
            qss = style.theme
        elif fr['theme'] == 'dark':
            from file_renamer.themes.dark.dark_linux import DarkLinux
            style = DarkLinux()
            qss = style.theme
    app.setStyleSheet(qss)
    logger.info('theme set: %s', fr['theme'])
    app.exec()
