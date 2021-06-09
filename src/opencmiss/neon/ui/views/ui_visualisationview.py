# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'visualisationview.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from opencmiss.neon.ui.zincwidgets.sceneviewerwidget import SceneviewerWidget


class Ui_VisualisationView(object):
    def setupUi(self, shared_opengl_widget, VisualisationView):
        if not VisualisationView.objectName():
            VisualisationView.setObjectName(u"VisualisationView")
        VisualisationView.resize(477, 336)
        self.horizontalLayout = QHBoxLayout(VisualisationView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = SceneviewerWidget(VisualisationView, shared_opengl_widget)
        self.widget.setObjectName(u"widget")
        self.widget.setContextMenuPolicy(Qt.NoContextMenu)

        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(VisualisationView)

        QMetaObject.connectSlotsByName(VisualisationView)
    # setupUi

    def retranslateUi(self, VisualisationView):
        VisualisationView.setWindowTitle(QCoreApplication.translate("VisualisationView", u"Visualisation", None))
    # retranslateUi

