# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/simulationview.ui'
#
# Created: Wed Dec 16 15:25:08 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_SimulationView(object):
    def setupUi(self, SimulationView):
        SimulationView.setObjectName("SimulationView")
        SimulationView.resize(481, 245)
        self.gridLayout = QtGui.QGridLayout(SimulationView)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonConfigureSimulation = QtGui.QPushButton(SimulationView)
        self.pushButtonConfigureSimulation.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/neon/images/icons/applications-system-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonConfigureSimulation.setIcon(icon)
        self.pushButtonConfigureSimulation.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonConfigureSimulation.setObjectName("pushButtonConfigureSimulation")
        self.gridLayout.addWidget(self.pushButtonConfigureSimulation, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 186, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.stackedWidgetSimulationView = QtGui.QStackedWidget(SimulationView)
        self.stackedWidgetSimulationView.setObjectName("stackedWidgetSimulationView")
        self.gridLayout.addWidget(self.stackedWidgetSimulationView, 0, 1, 2, 1)

        self.retranslateUi(SimulationView)
        QtCore.QMetaObject.connectSlotsByName(SimulationView)

    def retranslateUi(self, SimulationView):
        SimulationView.setWindowTitle(QtGui.QApplication.translate("SimulationView", "Simulation", None, QtGui.QApplication.UnicodeUTF8))
