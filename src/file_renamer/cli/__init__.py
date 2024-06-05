import logging
import sys
import os
import platform
import inspect
from pathlib import Path
from PySide6.QtWidgets import QApplication
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
    logger.info('platform: %s', platform.system())

    # File Renamer dict
    fr = {
        "home": home,
        "logfile": logfile,
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

    # File Renamer app
    app = QApplication(sys.argv)

    # Default screen resolution
    width = 1280
    height = 720

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
        app.exec()
