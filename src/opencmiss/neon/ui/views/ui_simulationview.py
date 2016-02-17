# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/simulationview.ui'
#
# Created: Tue Jan 26 11:21:27 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_SimulationView(object):
    def setupUi(self, SimulationView):
        SimulationView.setObjectName("SimulationView")
        SimulationView.resize(562, 398)
        self.gridLayout = QtGui.QGridLayout(SimulationView)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 186, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.stackedWidgetSimulationView = QtGui.QStackedWidget(SimulationView)
        self.stackedWidgetSimulationView.setObjectName("stackedWidgetSimulationView")
        self.gridLayout.addWidget(self.stackedWidgetSimulationView, 0, 1, 2, 1)
        self.pushButtonVisualise = QtGui.QPushButton(SimulationView)
        self.pushButtonVisualise.setObjectName("pushButtonVisualise")
        self.gridLayout.addWidget(self.pushButtonVisualise, 1, 0, 1, 1)

        self.retranslateUi(SimulationView)
        QtCore.QMetaObject.connectSlotsByName(SimulationView)

    def retranslateUi(self, SimulationView):
        SimulationView.setWindowTitle(QtGui.QApplication.translate("SimulationView", "Simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonVisualise.setText(QtGui.QApplication.translate("SimulationView", "Visualise", None, QtGui.QApplication.UnicodeUTF8))
