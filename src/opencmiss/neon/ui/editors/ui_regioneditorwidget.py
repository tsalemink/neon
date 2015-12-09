# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'regioneditorwidget.ui'
#
# Created: Tue Dec 08 11:35:23 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RegionEditorWidget(object):
    def setupUi(self, RegionEditorWidget):
        RegionEditorWidget.setObjectName("RegionEditorWidget")
        RegionEditorWidget.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(RegionEditorWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeViewRegion = QtGui.QTreeView(RegionEditorWidget)
        self.treeViewRegion.setObjectName("treeViewRegion")
        self.verticalLayout.addWidget(self.treeViewRegion)

        self.retranslateUi(RegionEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(RegionEditorWidget)

    def retranslateUi(self, RegionEditorWidget):
        RegionEditorWidget.setWindowTitle(QtGui.QApplication.translate("RegionEditorWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))

