import logging
import sys
import os
import platform
import inspect
from pathlib import Path
from PySide6.QtWidgets import QApplication
from file_renamer import gui


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
    logger.info(__file__)
    function = inspect.stack()[0].function
    logger.info(function)
    logger.info('platform: %s', platform.system())

    # File Renamer dict
    fr = {
        "home": home,
        "platform": platform,
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
        "html_body": ""
    }

    # Launch app
    app = QApplication(sys.argv)
    window = gui.MainWindow(**fr)
    window.resize(1280, 720)
    window.show()
    app.exec()
