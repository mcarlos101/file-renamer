import logging
import sys
from PySide6.QtWidgets import QApplication
from file_renamer import gui


def start_app(**fr):
    logging.info('__init.py__')
    logging.info('%sstart_app()', fr['tab'])
    app = QApplication(sys.argv)
    window = gui.MainWindow(**fr)
    window.resize(1280, 720)
    window.show()
    app.exec()
