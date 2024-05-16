# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextEdit,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.browse = QGroupBox(Widget)
        self.browse.setObjectName(u"browse")
        self.browse.setFocusPolicy(Qt.StrongFocus)
        self.formLayout = QFormLayout(self.browse)
        self.formLayout.setObjectName(u"formLayout")
        self.dir_btn = QPushButton(self.browse)
        self.dir_btn.setObjectName(u"dir_btn")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.dir_btn)

        self.dir_txt = QLineEdit(self.browse)
        self.dir_txt.setObjectName(u"dir_txt")
        self.dir_txt.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.dir_txt)


        self.gridLayout.addWidget(self.browse, 0, 0, 1, 1)

        self.dir_output = QTextEdit(Widget)
        self.dir_output.setObjectName(u"dir_output")
        self.dir_output.setReadOnly(True)

        self.gridLayout.addWidget(self.dir_output, 1, 0, 1, 1)

        self.options = QGroupBox(Widget)
        self.options.setObjectName(u"options")
        self.horizontalLayout_3 = QHBoxLayout(self.options)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.recursively = QCheckBox(self.options)
        self.recursively.setObjectName(u"recursively")

        self.horizontalLayout_3.addWidget(self.recursively)

        self.id = QCheckBox(self.options)
        self.id.setObjectName(u"id")

        self.horizontalLayout_3.addWidget(self.id)

        self.extension = QCheckBox(self.options)
        self.extension.setObjectName(u"extension")

        self.horizontalLayout_3.addWidget(self.extension)


        self.gridLayout.addWidget(self.options, 2, 0, 1, 1)

        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.clear_btn = QPushButton(self.groupBox)
        self.clear_btn.setObjectName(u"clear_btn")

        self.horizontalLayout.addWidget(self.clear_btn)

        self.rename_btn = QPushButton(self.groupBox)
        self.rename_btn.setObjectName(u"rename_btn")
        self.rename_btn.setEnabled(False)

        self.horizontalLayout.addWidget(self.rename_btn)


        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 1)

        self.search_replace = QGroupBox(Widget)
        self.search_replace.setObjectName(u"search_replace")
        self.horizontalLayout_2 = QHBoxLayout(self.search_replace)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.search_label = QLabel(self.search_replace)
        self.search_label.setObjectName(u"search_label")

        self.horizontalLayout_2.addWidget(self.search_label)

        self.search = QLineEdit(self.search_replace)
        self.search.setObjectName(u"search")
        self.search.setTabletTracking(False)
        self.search.setFocusPolicy(Qt.StrongFocus)
        self.search.setText(u"")
        self.search.setPlaceholderText(u"")

        self.horizontalLayout_2.addWidget(self.search)

        self.replace_label = QLabel(self.search_replace)
        self.replace_label.setObjectName(u"replace_label")

        self.horizontalLayout_2.addWidget(self.replace_label)

        self.replace = QLineEdit(self.search_replace)
        self.replace.setObjectName(u"replace")
        self.replace.setTabletTracking(False)
        self.replace.setFocusPolicy(Qt.StrongFocus)

        self.horizontalLayout_2.addWidget(self.replace)

        self.regex = QCheckBox(self.search_replace)
        self.regex.setObjectName(u"regex")

        self.horizontalLayout_2.addWidget(self.regex)

        self.find_btn = QPushButton(self.search_replace)
        self.find_btn.setObjectName(u"find_btn")

        self.horizontalLayout_2.addWidget(self.find_btn)


        self.gridLayout.addWidget(self.search_replace, 4, 0, 1, 1)

        QWidget.setTabOrder(self.dir_btn, self.dir_txt)
        QWidget.setTabOrder(self.dir_txt, self.dir_output)
        QWidget.setTabOrder(self.dir_output, self.recursively)
        QWidget.setTabOrder(self.recursively, self.id)
        QWidget.setTabOrder(self.id, self.extension)
        QWidget.setTabOrder(self.extension, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.clear_btn)
        QWidget.setTabOrder(self.clear_btn, self.rename_btn)
        QWidget.setTabOrder(self.rename_btn, self.search)
        QWidget.setTabOrder(self.search, self.replace)
        QWidget.setTabOrder(self.replace, self.regex)
        QWidget.setTabOrder(self.regex, self.find_btn)

        self.retranslateUi(Widget)
        self.dir_btn.clicked.connect(Widget.open_dir)
        self.dir_btn.clicked.connect(self.dir_txt.update)
        self.clear_btn.clicked.connect(Widget.clear)
        self.comboBox.activated.connect(Widget.index_changed)
        self.rename_btn.clicked.connect(Widget.rename_files)
        self.recursively.clicked.connect(Widget.add_recursively)
        self.id.clicked.connect(Widget.keep_id)
        self.extension.clicked.connect(Widget.keep_ext)
        self.regex.clicked.connect(Widget.regex)
        self.find_btn.clicked.connect(Widget.find)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"File Renamer", None))
        self.browse.setTitle("")
        self.dir_btn.setText(QCoreApplication.translate("Widget", u"Browse", None))
        self.options.setTitle("")
        self.recursively.setText(QCoreApplication.translate("Widget", u"Add Files Recursively", None))
        self.id.setText(QCoreApplication.translate("Widget", u"Keep ID", None))
        self.extension.setText(QCoreApplication.translate("Widget", u"Keep Extension", None))
        self.groupBox.setTitle("")
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget", u"PREVIEW", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget", u"Remove Non-Alphanum Chars", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Widget", u"Remove Accents", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Widget", u"Trim Spaces", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Widget", u"Replace Spaces With Hyphens", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Widget", u"Replace Dots With Hyphens", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Widget", u"Replace Hyphens With Spaces", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Widget", u"Lower Case", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Widget", u"Title Case", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Widget", u"Remove ID", None))

        self.clear_btn.setText(QCoreApplication.translate("Widget", u"CLEAR", None))
        self.rename_btn.setText(QCoreApplication.translate("Widget", u"RENAME", None))
        self.search_replace.setTitle("")
        self.search_label.setText(QCoreApplication.translate("Widget", u"Search", None))
        self.replace_label.setText(QCoreApplication.translate("Widget", u"Replace", None))
        self.replace.setText("")
        self.regex.setText(QCoreApplication.translate("Widget", u"Regular Expression", None))
        self.find_btn.setText(QCoreApplication.translate("Widget", u"Find", None))
    # retranslateUi

