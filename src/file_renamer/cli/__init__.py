import logging
import sys
import os
import platform
import inspect
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir, QFile, QFileInfo, QIODevice, QTextStream
from file_renamer.gui import MainWindow
from file_renamer.version import __version__


def start_app(**fr):
    # Logs
    home = os.path.expanduser('~')
    logfile = Path(home + "/file-renamer.log")
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=logfile,
        encoding='utf-8',
        filemode='w',
        level=logging.DEBUG
    )
    logger.info('File Renamer %s Logs', __version__)
    logger.info('')
    logger.info(__file__)
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

    try:
        # Detect screen resolution
        detected_width, detected_height = app.primaryScreen().size().toTuple()
        logger.info('detected_width: %s', detected_width)
        logger.info('detected_height: %s', detected_height)
        if detected_width > width and detected_height > height:
            width = detected_width
            height = detected_height
    except Exception as err:
        print('See logs: ', logfile)
        logger.exception(err)
    else:
        logger.info('width: %s', width)
        logger.info('height: %s', height)
        window = MainWindow(**fr)
        window.resize(width, height)
        window.show()

        # Set theme
        qss = ""
        logger.info('fr["platform"]: %s', fr["platform"])
        if fr["platform"] == "Windows":
            if fr['theme'] == 'light':
                from file_renamer.themes.light.light_windows import (
                    LightWindows
                )
                style = LightWindows()
                qss = style.theme
                logger.info('qss: %s', qss)
            elif fr['theme'] == 'dark':
                from file_renamer.themes.dark.dark_windows import DarkWindows
                style = DarkWindows()
                qss = style.theme
                logger.info('qss: %s', qss)
        else:
            if fr['theme'] == 'light':
                from file_renamer.themes.light.light_linux import LightLinux
                style = LightLinux()
                qss = style.theme
                logger.info('qss: %s', qss)
            elif fr['theme'] == 'dark':
                from file_renamer.themes.dark.dark_linux import DarkLinux
                style = DarkLinux()
                qss = style.theme
                logger.info('qss: %s', qss)
        app.setStyleSheet(qss)
        logger.info('theme set: %s', fr['theme'])
        app.exec()
