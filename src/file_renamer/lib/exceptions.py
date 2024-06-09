import sys
import logging
import inspect
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QPushButton
from PySide6.QtCore import Slot


class Errors(QMainWindow):

    def __init__(self, **fr):
        super().__init__()

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.fr = fr
        button = QMessageBox.critical(
            self,
            self.fr['error-title'],
            self.fr['error-msg'],
        )
