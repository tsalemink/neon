# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/problemview.ui'
#
# Created: Thu Dec 24 10:15:31 2015
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
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditFilter = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout.addWidget(self.lineEditFilter)
        self.listViewProblems = QtGui.QListView(self.layoutWidget)
        self.listViewProblems.setObjectName("listViewProblems")
        self.verticalLayout.addWidget(self.listViewProblems)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonRun = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonRun.setObjectName("pushButtonRun")
        self.horizontalLayout.addWidget(self.pushButtonRun)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stackedWidgetProblemView = QtGui.QStackedWidget(self.splitter)
        self.stackedWidgetProblemView.setObjectName("stackedWidgetProblemView")
        self.horizontalLayout_2.addWidget(self.splitter)

        self.retranslateUi(ProblemView)
        QtCore.QMetaObject.connectSlotsByName(ProblemView)
        ProblemView.setTabOrder(self.pushButtonRun, self.lineEditFilter)
        ProblemView.setTabOrder(self.lineEditFilter, self.listViewProblems)

    def retranslateUi(self, ProblemView):
        ProblemView.setWindowTitle(QtGui.QApplication.translate("ProblemView", "Problem", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditFilter.setPlaceholderText(QtGui.QApplication.translate("ProblemView", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRun.setToolTip(QtGui.QApplication.translate("ProblemView", "Run the selected simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRun.setText(QtGui.QApplication.translate("ProblemView", "Run", None, QtGui.QApplication.UnicodeUTF8))

