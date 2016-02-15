# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logswindow.ui'
#
# Created: Wed Jan 20 14:07:51 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Logger(object):
    def setupUi(self, Logger):
        Logger.setObjectName("Logger")
        Logger.resize(851, 167)
        self.gridLayout = QtGui.QGridLayout(Logger)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(Logger)
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
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(Logger)
        QtCore.QObject.connect(self.clearAllButton, QtCore.SIGNAL("clicked()"), Logger.clearAll)
        QtCore.QObject.connect(self.copyButton, QtCore.SIGNAL("clicked()"), Logger.copyToClipboard)
        QtCore.QMetaObject.connectSlotsByName(Logger)

    def retranslateUi(self, Logger):
        Logger.setWindowTitle(QtGui.QApplication.translate("Logger", "Log viewer", None))
        self.groupBox.setTitle(QtGui.QApplication.translate("Logger", "Logger", None))
        self.clearAllButton.setText(QtGui.QApplication.translate("Logger", "Clear All", None))
        self.copyButton.setText(QtGui.QApplication.translate("Logger", "Copy To Clipboard", None))