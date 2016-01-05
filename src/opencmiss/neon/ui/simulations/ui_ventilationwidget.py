# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/simulations/ventilationwidget.ui'
#
# Created: Wed Jan  6 12:19:52 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_VentilationWidget(object):
    def setupUi(self, VentilationWidget):
        VentilationWidget.setObjectName("VentilationWidget")
        VentilationWidget.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(VentilationWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtGui.QPlainTextEdit(VentilationWidget)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(VentilationWidget)
        QtCore.QMetaObject.connectSlotsByName(VentilationWidget)

    def retranslateUi(self, VentilationWidget):
        VentilationWidget.setWindowTitle(QtGui.QApplication.translate("VentilationWidget", "Ventilation", None, QtGui.QApplication.UnicodeUTF8))

