# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/visualisationview.ui'
#
# Created: Tue Dec 15 10:51:25 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_VisualisationView(object):
    def setupUi(self, VisualisationView):
        VisualisationView.setObjectName("VisualisationView")
        VisualisationView.resize(477, 336)
        self.horizontalLayout = QtGui.QHBoxLayout(VisualisationView)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = SceneviewerWidget(VisualisationView)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(VisualisationView)
        QtCore.QMetaObject.connectSlotsByName(VisualisationView)

    def retranslateUi(self, VisualisationView):
        VisualisationView.setWindowTitle(QtGui.QApplication.translate("VisualisationView", "Visualisation", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.neon.ui.zincwidgets.sceneviewerwidget import SceneviewerWidget
