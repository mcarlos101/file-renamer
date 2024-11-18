import logging
import inspect
from file_renamer.themes.theme import Theme


class DarkWindows(Theme):

    def __init__(self):

        # Method name
        logging.info(inspect.stack()[0].function)

        self.theme = """
QWidget {
    background-color: #212529;
    color: white;
    font-style: normal;
    font-weight: bold;
    font-size: 11px;
}

QMenu {
    background-color: #212529;
    color: white;
    border: 1px solid gray;
}

QMenu::item {
    background-color: #212529;
    color: white;
    padding: 5px;
    font-size: 11px;
}

QMenu::item:selected {
    color: black;
    background-color: white;
    font-weight: bold;
}

QToolBar {
    background-color: #212529;
    color: white;
}

QGroupBox {
    border: 1px solid #444444;
    background-color: #333333;
}

QLabel {
    background-color: #212529;
    color: #dce0e4;
}

QLabel#label {
    color: black;
    background-color: #9e9e9e;
    font-weight: bold;
    padding: 3px;
}

QLabel#search_label, #replace_label {
    color: #dce0e4;
    font-weight: bold;
    padding: 3px 0px;
    border: 1px solid gray;
}

QLineEdit, QTextEdit {
    background-color: #212529;
    color: #dce0e4;
    border: 1px solid gray;
    padding: 3px 0px;
}

QCheckBox {
    color: #dce0e4;
}

QPushButton {
    background-color: #212529;
    color: #dce0e4;
    border: 1px solid gray;
    padding: 4px 5px;
}

QPushButton:hover {
    background-color: white;
    color: black;
    font-weight: bold;
    padding: 4px 5px;
}

QPushButton:pressed {
    background-color: #dce0e4;
    color: #212529;
}

QPushButton#rename_btn:hover {
    color: white;
    background-color: maroon;
    font-weight: bold;
    padding: 4px 5px;
}

QComboBox {
    background-color: #212529;
    color: #dce0e4;
    border: 1px solid gray;
    padding: 3px 5px;
}

QComboBox QAbstractItemView {
    border: none;
    background-color: #212529;
}

QComboBox::item {
    background-color: #212529;
    color: #dce0e4;
}

QComboBox::item:selected {
    background-color: #dce0e4;
    color: #212529;
}

QMessageBox {
    background-color: #212529;
    color: #dce0e4;
}
"""

    def validate(self, value):
        pass
