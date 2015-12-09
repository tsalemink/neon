# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/tessellationeditorwidget.ui'
#
# Created: Wed Dec  9 12:55:39 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TessellationEditorWidget(object):
    def setupUi(self, TessellationEditorWidget):
        TessellationEditorWidget.setObjectName("TessellationEditorWidget")
        TessellationEditorWidget.resize(613, 476)
        self.verticalLayout = QtGui.QVBoxLayout(TessellationEditorWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(TessellationEditorWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidgetTessellations = QtGui.QTableWidget(self.groupBox)
        self.tableWidgetTessellations.setAlternatingRowColors(True)
        self.tableWidgetTessellations.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidgetTessellations.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidgetTessellations.setShowGrid(False)
        self.tableWidgetTessellations.setColumnCount(0)
        self.tableWidgetTessellations.setObjectName("tableWidgetTessellations")
        self.tableWidgetTessellations.setColumnCount(0)
        self.tableWidgetTessellations.setRowCount(0)
        self.tableWidgetTessellations.horizontalHeader().setVisible(True)
        self.tableWidgetTessellations.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetTessellations.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableWidgetTessellations, 0, 0, 1, 3)
        self.pushButtonAddTessellation = QtGui.QPushButton(self.groupBox)
        self.pushButtonAddTessellation.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/neon/images/icons/list-add-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAddTessellation.setIcon(icon)
        self.pushButtonAddTessellation.setObjectName("pushButtonAddTessellation")
        self.gridLayout.addWidget(self.pushButtonAddTessellation, 1, 0, 1, 1)
        self.pushButtonDeleteTessellation = QtGui.QPushButton(self.groupBox)
        self.pushButtonDeleteTessellation.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/neon/images/icons/list-remove-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDeleteTessellation.setIcon(icon1)
        self.pushButtonDeleteTessellation.setObjectName("pushButtonDeleteTessellation")
        self.gridLayout.addWidget(self.pushButtonDeleteTessellation, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(510, 19, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBoxProperties = QtGui.QGroupBox(TessellationEditorWidget)
        self.groupBoxProperties.setObjectName("groupBoxProperties")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBoxProperties)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxDefaultTessellation = QtGui.QCheckBox(self.groupBoxProperties)
        self.checkBoxDefaultTessellation.setObjectName("checkBoxDefaultTessellation")
        self.verticalLayout_2.addWidget(self.checkBoxDefaultTessellation)
        self.checkBoxDefaultPointsTessellation = QtGui.QCheckBox(self.groupBoxProperties)
        self.checkBoxDefaultPointsTessellation.setObjectName("checkBoxDefaultPointsTessellation")
        self.verticalLayout_2.addWidget(self.checkBoxDefaultPointsTessellation)
        self.verticalLayout.addWidget(self.groupBoxProperties)

        self.retranslateUi(TessellationEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(TessellationEditorWidget)

    def retranslateUi(self, TessellationEditorWidget):
        TessellationEditorWidget.setWindowTitle(QtGui.QApplication.translate("TessellationEditorWidget", "Tessellation Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("TessellationEditorWidget", "Tessellations", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAddTessellation.setToolTip(QtGui.QApplication.translate("TessellationEditorWidget", "Add spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDeleteTessellation.setToolTip(QtGui.QApplication.translate("TessellationEditorWidget", "Remove spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxProperties.setTitle(QtGui.QApplication.translate("TessellationEditorWidget", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDefaultTessellation.setText(QtGui.QApplication.translate("TessellationEditorWidget", "Default Tessellation", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDefaultPointsTessellation.setText(QtGui.QApplication.translate("TessellationEditorWidget", "Default Points Tessellation", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.neon.ui import icons_rc
