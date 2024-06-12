import sys
import logging
import inspect
from PySide6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QPushButton
)
from PySide6.QtCore import Slot


class Messages(QMainWindow):

    def __init__(self, **fr):
        super().__init__()

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.fr = fr
        if self.fr['msg-type'] == 'info':
            self.info()
        elif self.fr['msg-type'] == 'critical':
            self.critical()

    def info(self):
        button = QMessageBox.information(
            self,
            self.fr['msg-title'],
            self.fr['msg-info'],
        )

    def critical(self):
        button = QMessageBox.critical(
            self,
            self.fr['msg-title'],
            self.fr['msg-info'],
        )
