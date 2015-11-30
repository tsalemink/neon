# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/defaultview.ui'
#
# Created: Tue Dec  1 08:53:54 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DefaultView(object):
    def setupUi(self, DefaultView):
        DefaultView.setObjectName("DefaultView")
        DefaultView.resize(477, 336)
        self.horizontalLayout = QtGui.QHBoxLayout(DefaultView)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = SceneviewerWidget(DefaultView)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(DefaultView)
        QtCore.QMetaObject.connectSlotsByName(DefaultView)

    def retranslateUi(self, DefaultView):
        DefaultView.setWindowTitle(QtGui.QApplication.translate("DefaultView", "Default", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.neon.ui.zincwidgets.sceneviewerwidget import SceneviewerWidget
