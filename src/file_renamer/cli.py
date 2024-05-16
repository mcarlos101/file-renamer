import sys
from PySide6.QtWidgets import QApplication
import file_renamer.gui


def cli():
    app = QApplication(sys.argv)
    window = file_renamer.gui.MainWindow()
    window.resize(800, 600)
    window.show()
    app.exec()


if __name__ == "__main__":
    file_renamer.cli.cli()
