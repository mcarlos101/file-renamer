import logging
import sys
from PySide6.QtWidgets import QApplication
from file_renamer import gui


def start_app(**params):
    logging.info('__init.py__')
    logging.info('%sstart_app', params['tab'])
    app = QApplication(sys.argv)
    window = gui.MainWindow(**params)
    window.resize(1280, 720)
    window.show()
    app.exec()
