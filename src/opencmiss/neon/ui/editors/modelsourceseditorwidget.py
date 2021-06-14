'''
   Copyright 2015 University of Auckland

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
"""
Neon Model Sources Editor Widget

Dialog for creation and editing list of model sources (files/resources)
read into a region in Qt / Python.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from PySide2 import QtGui,QtWidgets

# from opencmiss.neon.core.neonregion import NeonRegion
from opencmiss.neon.core.neonmodelsources import NeonModelSourceFile

from opencmiss.neon.ui.editors.ui_modelsourceseditorwidget import Ui_ModelSourcesEditorWidget
from opencmiss.neon.core.neonlogger import NeonLogger


class ModelSourcesEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        '''
        Call the super class init functions
        '''
        QtWidgets.QWidget.__init__(self, parent)
        self._region = None
        self._currentModelSource = None
        self._itemModel = None
        # Using composition to include the visual element of the GUI.
        self._ui = Ui_ModelSourcesEditorWidget()
        self._ui.setupUi(self)
        # Extra UI code not possible with Designer
        self._ui.action_Hello = QtWidgets.QAction(self)
        self._ui.action_Hello.setText("Hello")

        self._ui.addMenu = QtWidgets.QMenu(self._ui.frame)
        self._ui.addMenu.setTitle("Bob")
        self._ui.addMenu.addAction(self._ui.action_Hello)
        self._ui.addMenu.show()
        self._ui.horizontalLayout.addWidget(self._ui.addMenu)
        # self._ui.addMenu = QtGui.QMenu(self._ui.frame)


        self._makeConnections()

    def _makeConnections(self):
        self._ui.listViewModelSources.clicked.connect(self._listSourceItemClicked)
        self._ui.comboBoxAddSource.currentIndexChanged.connect(self._addSourceEntered)
        self._ui.pushButtonApplySource.clicked.connect(self._applySourceClicked)
        self._ui.pushButtonDeleteSource.clicked.connect(self._deleteSourceClicked)
        self._ui.pushButtonBrowseFileName.clicked.connect(self._fileBrowseClicked)
        self._ui.lineEditTime.editingFinished.connect(self._fileTimeEntered)

    def getRegion(self):
        return self._region

    def setRegion(self, region):
        """
        :param region: NeonRegion to edit model sources for
        """
        self._region = region
        self._buildSourcesList()

    def _buildSourcesList(self):
        """
        Fill the list view with the list of model sources for current region
        """
        self._itemModel = QtGui.QStandardItemModel(self._ui.listViewModelSources)
        currentIndex = None
        modelSources = []
        if self._region:
            modelSources = self._region.getModelSources()
            # selectedGraphics = self.ui.graphics_editor.getGraphics()
            for modelSource in modelSources:
                name = modelSource.getDisplayName()
                item = QtGui.QStandardItem(name)
                item.setData(modelSource)
                item.setEditable(False)
                self._itemModel.appendRow(item)
                if modelSource == self._currentModelSource:
                    currentIndex = self._itemModel.indexFromItem(item)
        self._ui.listViewModelSources.setModel(self._itemModel)
        print(self._itemModel)
        if currentIndex is None:
            if len(modelSources) > 0:
                modelSource = modelSources[0]
                currentIndex = self._itemModel.createIndex(0, 0, self._itemModel.item(0))
            else:
                modelSource = None
            self._setCurrentModelSource(modelSource)
        if currentIndex is not None:
            print(currentIndex)
            print(self._ui.listViewModelSources)
            self._ui.listViewModelSources.setCurrentIndex(currentIndex)
            print("currentIndex")
        self._ui.listViewModelSources.show()

    def _refreshCurrentItem(self):
        if self._currentModelSource:
            name = self._currentModelSource.getDisplayName()
            currentIndex = self._ui.listViewModelSources.currentIndex()
            item = self._itemModel.item(currentIndex.row())
            item.setText(name)

    def _listSourceItemClicked(self, modelIndex):
        """
        Item in list of model sources selected
        """
        model = modelIndex.model()
        item = model.item(modelIndex.row())
        modelSource = item.data()
        self._setCurrentModelSource(modelSource)

    def _addSourceEntered(self, index):
        """
        Add a new model source with type given in name
        """
        if not self._region:
            return
        name = self._ui.comboBoxAddSource.currentText()
        modelSource = None
        if name == "File":
            modelSource = NeonModelSourceFile(fileName="")
            modelSource.setEdit(True)
        if modelSource:
            self._region.addModelSource(modelSource)
            self._setCurrentModelSource(modelSource)
            self._buildSourcesList()
        self._ui.comboBoxAddSource.setCurrentIndex(0)  # reset combo box we're using as a menu

    def _applySourceClicked(self):
        if self._region and self._currentModelSource:
            rebuildRegion = self._region.applyModelSource(self._currentModelSource)
            self._ui.pushButtonApplySource.setEnabled(self._currentModelSource.isEdit())
            self._refreshCurrentItem()

    def _deleteSourceClicked(self):
        if self._region and self._currentModelSource:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Neon: Please confirm")
            msgBox.setText("Delete model data source?")
            # msgBox.setInformativeText("Please confirm action.")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            result = msgBox.exec_()
            if result == QtWidgets.QMessageBox.Ok:
                self._region.removeModelSource(self._currentModelSource)

    def _setCurrentModelSource(self, modelSource):
        if modelSource is not self._currentModelSource:
            self._currentModelSource = modelSource
            isFileType = False
            if modelSource:
                self._ui.pushButtonApplySource.setEnabled(modelSource.isEdit())
                isFileType = modelSource.getType() == "FILE"
                if isFileType:
                    self._fileNameDisplay()
                    self._fileTimeDisplay()
            self._ui.groupBoxFileSource.setVisible(isFileType)
        elif not modelSource:
            self._ui.groupBoxFileSource.setVisible(False)

    def _editedCurrentModelSource(self):
        if self._currentModelSource:
            self._currentModelSource.setEdit(True)
            self._refreshCurrentItem()
            self._ui.pushButtonApplySource.setEnabled(True)

    def _fileNameDisplay(self):
        if self._currentModelSource:
            fileName = self._currentModelSource.getFileName()
            self._ui.lineEditFileName.setText(fileName)

    def _fileBrowseClicked(self):
        fileNameTuple = QtWidgets.QFileDialog.getOpenFileName(self, "Select Model Source", "", "Model Files (*.ex* *.fieldml)")
        fileName = fileNameTuple[0]
        # fileFilter = fileNameTuple[1]
        if not fileName:
            return
        self._currentModelSource.setFileName(fileName)
        self._editedCurrentModelSource()
        # set current directory to path from file, to support scripts and fieldml with external resources
        self._fileNameDisplay()

    def _fileTimeDisplay(self):
        if self._currentModelSource:
            time = self._currentModelSource.getTime()
            text = "{:.5g}".format(time) if time is not None else ""
            self._ui.lineEditTime.setText(text)

    def _fileTimeEntered(self):
        timeText = self._ui.lineEditTime.text().strip()
        try:
            if timeText == "":
                time = None
            else:
                time = float(timeText)
            self._currentModelSource.setTime(time)
            self._editedCurrentModelSource()
        except:
             NeonLogger.getLogger().error("Invalid time", timeText)
        self._fileTimeDisplay()
