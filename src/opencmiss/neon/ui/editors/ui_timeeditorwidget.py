# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/timeeditorwidget.ui'
#
# Created: Wed Dec  9 14:19:44 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeEditorWidget(object):
    def setupUi(self, TimeEditorWidget):
        TimeEditorWidget.setObjectName("TimeEditorWidget")
        TimeEditorWidget.resize(853, 85)
        self.horizontalLayout = QtGui.QHBoxLayout(TimeEditorWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtGui.QGroupBox(TimeEditorWidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEditTimer = QtGui.QLineEdit(self.groupBox)
        self.lineEditTimer.setObjectName("lineEditTimer")
        self.horizontalLayout_2.addWidget(self.lineEditTimer)
        self.horizontalSliderTimer = QtGui.QSlider(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSliderTimer.sizePolicy().hasHeightForWidth())
        self.horizontalSliderTimer.setSizePolicy(sizePolicy)
        self.horizontalSliderTimer.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderTimer.setObjectName("horizontalSliderTimer")
        self.horizontalLayout_2.addWidget(self.horizontalSliderTimer)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(TimeEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(TimeEditorWidget)

    def retranslateUi(self, TimeEditorWidget):
        TimeEditorWidget.setWindowTitle(QtGui.QApplication.translate("TimeEditorWidget", "Time Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("TimeEditorWidget", "Timer", None, QtGui.QApplication.UnicodeUTF8))

