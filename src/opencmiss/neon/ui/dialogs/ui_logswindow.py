# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logswindow.ui'
#
# Created: Wed Jan 20 14:07:51 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LogsWindow(object):
    def setupUi(self, LogsWindow):
        LogsWindow.setObjectName("LogsWindow")
        LogsWindow.resize(851, 167)
        self.gridLayout = QtGui.QGridLayout(LogsWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(LogsWindow)
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
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(LogsWindow)
        QtCore.QMetaObject.connectSlotsByName(LogsWindow)

        self.retranslateUi(LogsWindow)
        QtCore.QMetaObject.connectSlotsByName(LogsWindow)

    def retranslateUi(self, LogsWindow):
        LogsWindow.setWindowTitle(QtGui.QApplication.translate("LogsWindow", "Log viewer", None))
        self.groupBox.setTitle(QtGui.QApplication.translate("LogsWindow", "Logs", None))
        self.clearAllButton.setText(QtGui.QApplication.translate("LogsWindow", "Clear All", None))
