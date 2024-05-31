from PySide6.QtCore import Slot


class AppError(Exception):
    """ Custom exception class """

    def __init__(self, parent=None):
        self.msg = "ERROR!"

    @Slot()
    def print(self, **fr):
        fr["ui"].rename_btn.setEnabled(False)
        fr["ui"].dir_output.clear()
        style = "color: red;" "font-weight: bold;"
        if len(fr["msg"]):
            msg = '<span style="' + style + '">' + fr["msg"] + '</span>'
            fr["ui"].dir_output.append(msg)
        else:
            fr["ui"].dir_output.append(self.msg)
            self.msg = '<span style="' + style + '">' + self.msg + '</span>'
