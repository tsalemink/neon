# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newprojectdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_NewProjectDialog(object):
    def setupUi(self, NewProjectDialog):
        if not NewProjectDialog.objectName():
            NewProjectDialog.setObjectName(u"NewProjectDialog")
        NewProjectDialog.resize(509, 418)
        self.gridLayout = QGridLayout(NewProjectDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listViewProjects = QListView(NewProjectDialog)
        self.listViewProjects.setObjectName(u"listViewProjects")
        self.listViewProjects.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listViewProjects.setIconSize(QSize(24, 24))
        self.listViewProjects.setViewMode(QListView.ListMode)

        self.gridLayout.addWidget(self.listViewProjects, 1, 0, 1, 1)

        self.line = QFrame(NewProjectDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonOpen = QPushButton(NewProjectDialog)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")

        self.horizontalLayout.addWidget(self.pushButtonOpen)

        self.toolButtonRecent = QToolButton(NewProjectDialog)
        self.toolButtonRecent.setObjectName(u"toolButtonRecent")
        self.toolButtonRecent.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButtonRecent.setArrowType(Qt.NoArrow)

        self.horizontalLayout.addWidget(self.toolButtonRecent)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(NewProjectDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.lineEditFilter = QLineEdit(NewProjectDialog)
        self.lineEditFilter.setObjectName(u"lineEditFilter")

        self.gridLayout.addWidget(self.lineEditFilter, 0, 0, 1, 1)


        self.retranslateUi(NewProjectDialog)
        self.buttonBox.accepted.connect(NewProjectDialog.accept)

        QMetaObject.connectSlotsByName(NewProjectDialog)
    # setupUi

    def retranslateUi(self, NewProjectDialog):
        NewProjectDialog.setWindowTitle(QCoreApplication.translate("NewProjectDialog", u"New Project", None))
        self.pushButtonOpen.setText(QCoreApplication.translate("NewProjectDialog", u"Open", None))
        self.toolButtonRecent.setText(QCoreApplication.translate("NewProjectDialog", u"Recent ", None))
        self.lineEditFilter.setPlaceholderText(QCoreApplication.translate("NewProjectDialog", u"Filter", None))
    # retranslateUi

