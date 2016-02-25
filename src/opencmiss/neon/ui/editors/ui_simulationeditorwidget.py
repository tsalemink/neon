# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/editors/simulationeditorwidget.ui'
#
# Created: Thu Feb 25 20:26:40 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SimulationEditorWidget(object):
    def setupUi(self, SimulationEditorWidget):
        SimulationEditorWidget.setObjectName("SimulationEditorWidget")
        SimulationEditorWidget.resize(400, 300)
        self.formLayout = QtGui.QFormLayout(SimulationEditorWidget)
        self.formLayout.setObjectName("formLayout")
        self.pushButtonVisualise = QtGui.QPushButton(SimulationEditorWidget)
        self.pushButtonVisualise.setObjectName("pushButtonVisualise")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.pushButtonVisualise)

        self.retranslateUi(SimulationEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(SimulationEditorWidget)

    def retranslateUi(self, SimulationEditorWidget):
        SimulationEditorWidget.setWindowTitle(QtGui.QApplication.translate("SimulationEditorWidget", "Simulation Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonVisualise.setText(QtGui.QApplication.translate("SimulationEditorWidget", "Visualise", None, QtGui.QApplication.UnicodeUTF8))

