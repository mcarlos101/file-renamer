import logging
import sys
import inspect
from PySide6.QtWidgets import QApplication
from file_renamer import gui


def start_app(**fr):
    logging.info("")
    logging.info(__file__)
    function = inspect.stack()[0].function
    logging.info(function)
    app = QApplication(sys.argv)
    window = gui.MainWindow(**fr)
    window.resize(1280, 720)
    window.show()
    app.exec()
