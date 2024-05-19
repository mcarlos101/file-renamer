import sys
from PySide6.QtWidgets import QApplication
from file_renamer import gui


def start_app():
    app = QApplication(sys.argv)
    window = gui.MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()
