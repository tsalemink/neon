# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/loggerdialog.ui'
#
# Created: Wed Feb 24 21:07:01 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LoggerDialog(object):
    def setupUi(self, LoggerDialog):
        LoggerDialog.setObjectName("LoggerDialog")
        LoggerDialog.resize(851, 178)
        self.gridLayout = QtGui.QGridLayout(LoggerDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(LoggerDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.logText = QtGui.QTextBrowser(self.groupBox)
        self.logText.setObjectName("logText")
        self.gridLayout_2.addWidget(self.logText, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clearAllButton = QtGui.QPushButton(self.groupBox)
        self.clearAllButton.setObjectName("clearAllButton")
        self.horizontalLayout.addWidget(self.clearAllButton)
        self.copyButton = QtGui.QPushButton(self.groupBox)
        self.copyButton.setObjectName("copyButton")
        self.horizontalLayout.addWidget(self.copyButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(LoggerDialog)
        QtCore.QObject.connect(self.clearAllButton, QtCore.SIGNAL("clicked()"), LoggerDialog.clearAll)
        QtCore.QObject.connect(self.copyButton, QtCore.SIGNAL("clicked()"), LoggerDialog.copyToClipboard)
        QtCore.QMetaObject.connectSlotsByName(LoggerDialog)

    def retranslateUi(self, LoggerDialog):
        LoggerDialog.setWindowTitle(QtGui.QApplication.translate("LoggerDialog", "Log viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LoggerDialog", "Logger", None, QtGui.QApplication.UnicodeUTF8))
        self.clearAllButton.setText(QtGui.QApplication.translate("LoggerDialog", "Clear All", None, QtGui.QApplication.UnicodeUTF8))
        self.copyButton.setText(QtGui.QApplication.translate("LoggerDialog", "Copy To Clipboard", None, QtGui.QApplication.UnicodeUTF8))
