import logging
import inspect
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox
)


class Messages(QMainWindow):

    def __init__(self, **fr):
        super().__init__()
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
