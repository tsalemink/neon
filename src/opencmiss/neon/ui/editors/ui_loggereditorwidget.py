# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loggereditorwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  opencmiss.neon.ui import icons_rc

class Ui_LoggerEditorWidget(object):
    def setupUi(self, LoggerEditorWidget):
        if not LoggerEditorWidget.objectName():
            LoggerEditorWidget.setObjectName(u"LoggerEditorWidget")
        LoggerEditorWidget.resize(670, 384)
        self.gridLayout = QGridLayout(LoggerEditorWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(LoggerEditorWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.logText = QTextBrowser(self.groupBox)
        self.logText.setObjectName(u"logText")

        self.gridLayout_2.addWidget(self.logText, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clearAllButton = QPushButton(self.groupBox)
        self.clearAllButton.setObjectName(u"clearAllButton")

        self.horizontalLayout.addWidget(self.clearAllButton)

        self.copyButton = QPushButton(self.groupBox)
        self.copyButton.setObjectName(u"copyButton")

        self.horizontalLayout.addWidget(self.copyButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)


        self.retranslateUi(LoggerEditorWidget)
        self.clearAllButton.clicked.connect(LoggerEditorWidget.clearAll)
        self.copyButton.clicked.connect(LoggerEditorWidget.copyToClipboard)

        QMetaObject.connectSlotsByName(LoggerEditorWidget)
    # setupUi

    def retranslateUi(self, LoggerEditorWidget):
        LoggerEditorWidget.setWindowTitle(QCoreApplication.translate("LoggerEditorWidget", u"Log viewer", None))
        self.groupBox.setTitle(QCoreApplication.translate("LoggerEditorWidget", u"Logger", None))
        self.clearAllButton.setText(QCoreApplication.translate("LoggerEditorWidget", u"Clear All", None))
        self.copyButton.setText(QCoreApplication.translate("LoggerEditorWidget", u"Copy To Clipboard", None))
    # retranslateUi

