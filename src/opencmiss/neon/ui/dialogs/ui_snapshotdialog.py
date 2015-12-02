# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/designer/snapshotdialog.ui'
#
# Created: Tue Dec  1 15:08:10 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SnapshotDialog(object):
    def setupUi(self, SnapshotDialog):
        SnapshotDialog.setObjectName("SnapshotDialog")
        SnapshotDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(SnapshotDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(SnapshotDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBoxHeight = QtGui.QSpinBox(self.groupBox)
        self.spinBoxHeight.setEnabled(False)
        self.spinBoxHeight.setObjectName("spinBoxHeight")
        self.gridLayout.addWidget(self.spinBoxHeight, 2, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditFilename = QtGui.QLineEdit(self.groupBox)
        self.lineEditFilename.setObjectName("lineEditFilename")
        self.horizontalLayout.addWidget(self.lineEditFilename)
        self.pushButtonFilename = QtGui.QPushButton(self.groupBox)
        self.pushButtonFilename.setObjectName("pushButtonFilename")
        self.horizontalLayout.addWidget(self.pushButtonFilename)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 3)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBoxWidth = QtGui.QSpinBox(self.groupBox)
        self.spinBoxWidth.setEnabled(False)
        self.spinBoxWidth.setObjectName("spinBoxWidth")
        self.gridLayout.addWidget(self.spinBoxWidth, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.checkBoxWYSIWYG = QtGui.QCheckBox(self.groupBox)
        self.checkBoxWYSIWYG.setChecked(True)
        self.checkBoxWYSIWYG.setObjectName("checkBoxWYSIWYG")
        self.gridLayout.addWidget(self.checkBoxWYSIWYG, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widgetPreview = SceneviewerWidget(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widgetPreview.sizePolicy().hasHeightForWidth())
        self.widgetPreview.setSizePolicy(sizePolicy)
        self.widgetPreview.setMinimumSize(QtCore.QSize(50, 50))
        self.widgetPreview.setObjectName("widgetPreview")
        self.horizontalLayout_2.addWidget(self.widgetPreview)
        self.gridLayout.addWidget(self.groupBox_2, 0, 2, 4, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(SnapshotDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SnapshotDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SnapshotDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SnapshotDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SnapshotDialog)

    def retranslateUi(self, SnapshotDialog):
        SnapshotDialog.setWindowTitle(QtGui.QApplication.translate("SnapshotDialog", "Snapshot", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SnapshotDialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SnapshotDialog", "Height (px):", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SnapshotDialog", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonFilename.setText(QtGui.QApplication.translate("SnapshotDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SnapshotDialog", "Width (px):", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxWYSIWYG.setToolTip(QtGui.QApplication.translate("SnapshotDialog", "What you see is what you get!", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxWYSIWYG.setText(QtGui.QApplication.translate("SnapshotDialog", "WYSIWYG", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SnapshotDialog", "Preview", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.neon.ui.zincwidgets.sceneviewerwidget import SceneviewerWidget
