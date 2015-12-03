# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/spectrumeditorwidget.ui'
#
# Created: Thu Dec  3 13:53:59 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SpectrumEditorWidget(object):
    def setupUi(self, SpectrumEditorWidget):
        SpectrumEditorWidget.setObjectName("SpectrumEditorWidget")
        SpectrumEditorWidget.resize(281, 744)
        self.verticalLayout = QtGui.QVBoxLayout(SpectrumEditorWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(SpectrumEditorWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidgetSpectrums = QtGui.QListWidget(self.groupBox)
        self.listWidgetSpectrums.setObjectName("listWidgetSpectrums")
        self.gridLayout.addWidget(self.listWidgetSpectrums, 0, 0, 1, 3)
        self.pushButtonAddSpectrum = QtGui.QPushButton(self.groupBox)
        self.pushButtonAddSpectrum.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/neon/images/icons/list-add-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAddSpectrum.setIcon(icon)
        self.pushButtonAddSpectrum.setObjectName("pushButtonAddSpectrum")
        self.gridLayout.addWidget(self.pushButtonAddSpectrum, 1, 0, 1, 1)
        self.pushButtonDeleteSpectrum = QtGui.QPushButton(self.groupBox)
        self.pushButtonDeleteSpectrum.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/neon/images/icons/list-remove-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDeleteSpectrum.setIcon(icon1)
        self.pushButtonDeleteSpectrum.setObjectName("pushButtonDeleteSpectrum")
        self.gridLayout.addWidget(self.pushButtonDeleteSpectrum, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(SpectrumEditorWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox = QtGui.QComboBox(self.groupBox_2)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(SpectrumEditorWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = SceneviewerWidget(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(SpectrumEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(SpectrumEditorWidget)

    def retranslateUi(self, SpectrumEditorWidget):
        SpectrumEditorWidget.setWindowTitle(QtGui.QApplication.translate("SpectrumEditorWidget", "Spectrum Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SpectrumEditorWidget", "Spectrums", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SpectrumEditorWidget", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SpectrumEditorWidget", "Colour Map:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("SpectrumEditorWidget", "Preview", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.neon.ui.zincwidgets.sceneviewerwidget import SceneviewerWidget
from opencmiss.neon.ui import icons_rc
