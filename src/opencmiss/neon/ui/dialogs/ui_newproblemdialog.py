# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/newproblemdialog.ui'
#
# Created: Thu Feb 25 08:16:10 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewProblemDialog(object):
    def setupUi(self, NewProblemDialog):
        NewProblemDialog.setObjectName("NewProblemDialog")
        NewProblemDialog.resize(509, 418)
        self.gridLayout = QtGui.QGridLayout(NewProblemDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listViewProblems = QtGui.QListView(NewProblemDialog)
        self.listViewProblems.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listViewProblems.setIconSize(QtCore.QSize(24, 24))
        self.listViewProblems.setViewMode(QtGui.QListView.ListMode)
        self.listViewProblems.setObjectName("listViewProblems")
        self.gridLayout.addWidget(self.listViewProblems, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonOpen = QtGui.QPushButton(NewProblemDialog)
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.horizontalLayout.addWidget(self.pushButtonOpen)
        self.toolButtonRecent = QtGui.QToolButton(NewProblemDialog)
        self.toolButtonRecent.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonRecent.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonRecent.setObjectName("toolButtonRecent")
        self.horizontalLayout.addWidget(self.toolButtonRecent)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(NewProblemDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.line = QtGui.QFrame(NewProblemDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.retranslateUi(NewProblemDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewProblemDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(NewProblemDialog)

    def retranslateUi(self, NewProblemDialog):
        NewProblemDialog.setWindowTitle(QtGui.QApplication.translate("NewProblemDialog", "New Problem", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOpen.setText(QtGui.QApplication.translate("NewProblemDialog", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonRecent.setText(QtGui.QApplication.translate("NewProblemDialog", "Recent ", None, QtGui.QApplication.UnicodeUTF8))

