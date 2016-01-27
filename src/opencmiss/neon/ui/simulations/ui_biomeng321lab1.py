# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/simulations/biomeng321lab1.ui'
#
# Created: Wed Jan 27 10:57:15 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Biomeng321Lab1(object):
    def setupUi(self, Biomeng321Lab1):
        Biomeng321Lab1.setObjectName("Biomeng321Lab1")
        Biomeng321Lab1.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Biomeng321Lab1)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(Biomeng321Lab1)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Biomeng321Lab1)
        QtCore.QMetaObject.connectSlotsByName(Biomeng321Lab1)

    def retranslateUi(self, Biomeng321Lab1):
        Biomeng321Lab1.setWindowTitle(QtGui.QApplication.translate("Biomeng321Lab1", "Biomeng321 Lab1", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Biomeng321Lab1", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Biomeng321Lab1", "Stress:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Biomeng321Lab1", "Strain:", None, QtGui.QApplication.UnicodeUTF8))

