import logging
import inspect
from pathlib import Path
from abc import ABC, abstractmethod
from file_renamer.themes.theme import Theme


class LightWindows(Theme):

    def __init__(self):

        # Log file, class & method names
        logging.info("")
        logging.info(__file__)
        logging.info(self.__class__.__qualname__)
        logging.info(inspect.stack()[0].function)

        self.theme = """
QWidget {
    background-color: white;
    color: black;
    font-style: normal;
    font-weight: bold;
    font-size: 11px;
}

QMenu {
    background-color: white;
    color: black;
    border: 1px solid gray;
}

QMenu::item {
    background-color: transparent;
    padding: 5px;
    font-size: 11px;
}

QMenu::item:selected {
    color: white;
    background-color: black;
    font-weight: bold;
}

QToolBar {
    background-color: white;
    color: black;
}

QGroupBox {
    /* border: 1px solid gray;*/
}

QLabel {
    background-color: white;
    color: black;
}

QLabel#label {
    color: black;
    font-weight: bold;
}

QLabel#search_label, #replace_label {
    color: black;
    font-weight: bold;
    padding: 3px 0px;
    border: 1px solid gray;
}

QLineEdit, QTextEdit {
    background-color: white;
    color: black;
}

QCheckBox {
    color: black;
}

QPushButton {
    background-color: white;
    color: black;
    padding: 4px 5px;
}

QPushButton:hover {
    background-color: black;
    color: white;
    font-weight: bold;
    padding: 4px 5px;
}

QPushButton:pressed {
    background-color: white;
    color: black;
}

QComboBox {
    background-color: white;
    color: black;
}

QComboBox QAbstractItemView {
    border: none;
    background-color: white;
}

QComboBox::item {
    background-color: white;
    color: black;
}

QComboBox::item:selected {
    background-color: black;
    color: white;
}

QMessageBox {
    background-color: white;
    color: black;
}

"""

    def validate(self, value):
        logging.info(inspect.stack()[0].function)  # method name
        logging.info("validate")
