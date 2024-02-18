from PySide6.QtCore import Slot

class AppError(Exception):
    """ Custom exception class """

    def __init__(self, parent=None):
        self.msg = "ERROR!"

    @Slot()
    def print(self, ui, msg):
        ui.rename_btn.setEnabled(False)
        ui.dir_output.clear()
        style = "color: red;" "font-weight: bold;"
        if len(msg):
            msg =  '<span style="' + style + '">' + msg + '</span>'
            ui.dir_output.append(msg)
        else:
            ui.dir_output.append(self.msg)
            self.msg =  '<span style="' + style + '">' + self.msg + '</span>'

