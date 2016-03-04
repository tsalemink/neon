# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/visualisationview.ui'
#
# Created: Mon Jan 25 15:25:10 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_VisualisationView(object):
    def setupUi(self, shared_opengl_widget, VisualisationView):
        VisualisationView.setObjectName("VisualisationView")
        VisualisationView.resize(477, 336)
        self.horizontalLayout = QtGui.QHBoxLayout(VisualisationView)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = SceneviewerWidget(VisualisationView, shared_opengl_widget)
        self.widget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(VisualisationView)
        QtCore.QMetaObject.connectSlotsByName(VisualisationView)

    def retranslateUi(self, VisualisationView):
        VisualisationView.setWindowTitle(QtGui.QApplication.translate("VisualisationView", "Visualisation", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.neon.ui.zincwidgets.sceneviewerwidget import SceneviewerWidget
