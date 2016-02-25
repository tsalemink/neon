# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/problemview.ui'
#
# Created: Thu Feb 25 14:37:56 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ProblemView(object):
    def setupUi(self, ProblemView):
        ProblemView.setObjectName("ProblemView")
        ProblemView.resize(584, 469)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(ProblemView)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtGui.QSplitter(ProblemView)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.stackedWidgetProblemView = QtGui.QStackedWidget(self.splitter)
        self.stackedWidgetProblemView.setObjectName("stackedWidgetProblemView")
        self.horizontalLayout_2.addWidget(self.splitter)

        self.retranslateUi(ProblemView)
        QtCore.QMetaObject.connectSlotsByName(ProblemView)

    def retranslateUi(self, ProblemView):
        ProblemView.setWindowTitle(QtGui.QApplication.translate("ProblemView", "Problem", None, QtGui.QApplication.UnicodeUTF8))

