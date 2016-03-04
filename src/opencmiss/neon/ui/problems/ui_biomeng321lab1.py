# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/problems/biomeng321lab1.ui'
#
# Created: Mon Feb 15 13:12:24 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Biomeng321Lab1(object):
    def setupUi(self, Biomeng321Lab1):
        Biomeng321Lab1.setObjectName("Biomeng321Lab1")
        Biomeng321Lab1.resize(514, 427)
        self.gridLayout = QtGui.QGridLayout(Biomeng321Lab1)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(Biomeng321Lab1)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBoxBoundaryConditions = QtGui.QComboBox(self.groupBox)
        self.comboBoxBoundaryConditions.setObjectName("comboBoxBoundaryConditions")
        self.comboBoxBoundaryConditions.addItem("")
        self.comboBoxBoundaryConditions.addItem("")
        self.comboBoxBoundaryConditions.addItem("")
        self.comboBoxBoundaryConditions.addItem("")
        self.comboBoxBoundaryConditions.addItem("")
        self.gridLayout_2.addWidget(self.comboBoxBoundaryConditions, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.label_17 = QtGui.QLabel(self.groupBox)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Biomeng321Lab1)
        QtCore.QMetaObject.connectSlotsByName(Biomeng321Lab1)

    def retranslateUi(self, Biomeng321Lab1):
        Biomeng321Lab1.setWindowTitle(QtGui.QApplication.translate("Biomeng321Lab1", "Biomeng321 Lab1", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Biomeng321Lab1", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBoundaryConditions.setItemText(0, QtGui.QApplication.translate("Biomeng321Lab1", "Type 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBoundaryConditions.setItemText(1, QtGui.QApplication.translate("Biomeng321Lab1", "Type 2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBoundaryConditions.setItemText(2, QtGui.QApplication.translate("Biomeng321Lab1", "Type 3", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBoundaryConditions.setItemText(3, QtGui.QApplication.translate("Biomeng321Lab1", "Type 4", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBoundaryConditions.setItemText(4, QtGui.QApplication.translate("Biomeng321Lab1", "Type 5", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("Biomeng321Lab1", "Boundary conditions:", None, QtGui.QApplication.UnicodeUTF8))

