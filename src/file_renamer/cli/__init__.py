import sys
from PySide6.QtWidgets import QApplication
from file_renamer import gui


def start_app():
    app = QApplication(sys.argv)
    window = gui.MainWindow()
    window.resize(1280, 720)
    window.show()
    app.exec()
