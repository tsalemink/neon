# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/editors/problemeditorwidget.ui'
#
# Created: Thu Feb 25 19:48:59 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ProblemEditorWidget(object):
    def setupUi(self, ProblemEditorWidget):
        ProblemEditorWidget.setObjectName("ProblemEditorWidget")
        ProblemEditorWidget.resize(302, 154)
        self.formLayout = QtGui.QFormLayout(ProblemEditorWidget)
        self.formLayout.setObjectName("formLayout")
        self.pushButtonRun = QtGui.QPushButton(ProblemEditorWidget)
        self.pushButtonRun.setObjectName("pushButtonRun")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.pushButtonRun)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtGui.QFormLayout.LabelRole, spacerItem)

        self.retranslateUi(ProblemEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(ProblemEditorWidget)

    def retranslateUi(self, ProblemEditorWidget):
        ProblemEditorWidget.setWindowTitle(QtGui.QApplication.translate("ProblemEditorWidget", "Problem Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRun.setText(QtGui.QApplication.translate("ProblemEditorWidget", "Run", None, QtGui.QApplication.UnicodeUTF8))

