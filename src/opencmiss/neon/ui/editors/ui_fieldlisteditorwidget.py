# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fieldlisteditorwidget.ui'
#
# Created: Fri Apr 15 16:20:49 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FieldListEditorWidget(object):
    def setupUi(self, FieldListEditorWidget):
        FieldListEditorWidget.setObjectName("FieldListEditorWidget")
        FieldListEditorWidget.resize(300, 725)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FieldListEditorWidget.sizePolicy().hasHeightForWidth())
        FieldListEditorWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(FieldListEditorWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(FieldListEditorWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 294, 719))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.field_listview = QtGui.QListView(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.field_listview.sizePolicy().hasHeightForWidth())
        self.field_listview.setSizePolicy(sizePolicy)
        self.field_listview.setObjectName("field_listview")
        self.verticalLayout_2.addWidget(self.field_listview)
        self.frame = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addFieldButton = QtGui.QPushButton(self.frame)
        self.addFieldButton.setObjectName("addFieldButton")
        self.horizontalLayout.addWidget(self.addFieldButton)
        self.verticalLayout_2.addWidget(self.frame)
        self.field_editor = FieldEditorWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.field_editor.sizePolicy().hasHeightForWidth())
        self.field_editor.setSizePolicy(sizePolicy)
        self.field_editor.setObjectName("field_editor")
        self.verticalLayout_2.addWidget(self.field_editor)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(FieldListEditorWidget)

    def retranslateUi(self, FieldListEditorWidget):
        FieldListEditorWidget.setWindowTitle(QtGui.QApplication.translate("FieldListEditorWidget", "Field List Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.addFieldButton.setText(QtGui.QApplication.translate("FieldListEditorWidget", "Add Field", None, QtGui.QApplication.UnicodeUTF8))
        
from opencmiss.neon.ui.zincwidgets.fieldeditorwidget import FieldEditorWidget
