from PySide6.QtCore import Slot


class AppError(Exception):
    """ Custom exception class """

    def __init__(self, parent=None):
        self.msg = "ERROR!"

    @Slot()
    def print(self, **params):
        params["ui"].rename_btn.setEnabled(False)
        params["ui"].dir_output.clear()
        style = "color: red;" "font-weight: bold;"
        if len(params["msg"]):
            msg = '<span style="' + style + '">' + params["msg"] + '</span>'
            params["ui"].dir_output.append(msg)
        else:
            params["ui"].dir_output.append(self.msg)
            self.msg = '<span style="' + style + '">' + self.msg + '</span>'
