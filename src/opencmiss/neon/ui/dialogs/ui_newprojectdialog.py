# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/newprojectdialog.ui'
#
# Created: Thu Feb 25 14:40:35 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewProjectDialog(object):
    def setupUi(self, NewProjectDialog):
        NewProjectDialog.setObjectName("NewProjectDialog")
        NewProjectDialog.resize(509, 418)
        self.gridLayout = QtGui.QGridLayout(NewProjectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listViewProjects = QtGui.QListView(NewProjectDialog)
        self.listViewProjects.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listViewProjects.setIconSize(QtCore.QSize(24, 24))
        self.listViewProjects.setViewMode(QtGui.QListView.ListMode)
        self.listViewProjects.setObjectName("listViewProjects")
        self.gridLayout.addWidget(self.listViewProjects, 1, 0, 1, 1)
        self.line = QtGui.QFrame(NewProjectDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonOpen = QtGui.QPushButton(NewProjectDialog)
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.horizontalLayout.addWidget(self.pushButtonOpen)
        self.toolButtonRecent = QtGui.QToolButton(NewProjectDialog)
        self.toolButtonRecent.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButtonRecent.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonRecent.setObjectName("toolButtonRecent")
        self.horizontalLayout.addWidget(self.toolButtonRecent)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(NewProjectDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.lineEditFilter = QtGui.QLineEdit(NewProjectDialog)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.gridLayout.addWidget(self.lineEditFilter, 0, 0, 1, 1)

        self.retranslateUi(NewProjectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewProjectDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(NewProjectDialog)

    def retranslateUi(self, NewProjectDialog):
        NewProjectDialog.setWindowTitle(QtGui.QApplication.translate("NewProjectDialog", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOpen.setText(QtGui.QApplication.translate("NewProjectDialog", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonRecent.setText(QtGui.QApplication.translate("NewProjectDialog", "Recent ", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditFilter.setPlaceholderText(QtGui.QApplication.translate("NewProjectDialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))

