import logging
import inspect
from PySide6.QtCore import Slot


class AppError(Exception):
    """ Custom exception class """

    def __init__(self, parent=None):

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.msg = "ERROR!"

    @Slot()
    def print(self, **fr):
        logging.info(inspect.stack()[0].function)  # method name
        fr["ui"].rename_btn.setEnabled(False)
        fr["ui"].dir_output.clear()
        style = "color: red;" "font-weight: bold;"
        if len(fr["msg"]):
            msg = '<span style="' + style + '">' + fr["msg"] + '</span>'
            fr["ui"].dir_output.append(msg)
        else:
            fr["ui"].dir_output.append(self.msg)
            self.msg = '<span style="' + style + '">' + self.msg + '</span>'
