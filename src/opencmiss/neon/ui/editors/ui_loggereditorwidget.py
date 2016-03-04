# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res\designer\editors\loggereditorwidget.ui'
#
# Created: Thu Mar 03 13:47:15 2016
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LoggerEditorWidget(object):
    def setupUi(self, LoggerEditorWidget):
        LoggerEditorWidget.setObjectName("LoggerEditorWidget")
        LoggerEditorWidget.resize(851, 186)
        self.gridLayout = QtGui.QGridLayout(LoggerEditorWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(LoggerEditorWidget)
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

        self.retranslateUi(LoggerEditorWidget)
        QtCore.QObject.connect(self.clearAllButton, QtCore.SIGNAL("clicked()"), LoggerEditorWidget.clearAll)
        QtCore.QObject.connect(self.copyButton, QtCore.SIGNAL("clicked()"), LoggerEditorWidget.copyToClipboard)
        QtCore.QMetaObject.connectSlotsByName(LoggerEditorWidget)

    def retranslateUi(self, LoggerEditorWidget):
        LoggerEditorWidget.setWindowTitle(QtGui.QApplication.translate("LoggerEditorWidget", "Log viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LoggerEditorWidget", "Logger", None, QtGui.QApplication.UnicodeUTF8))
        self.clearAllButton.setText(QtGui.QApplication.translate("LoggerEditorWidget", "Clear All", None, QtGui.QApplication.UnicodeUTF8))
        self.copyButton.setText(QtGui.QApplication.translate("LoggerEditorWidget", "Copy To Clipboard", None, QtGui.QApplication.UnicodeUTF8))
