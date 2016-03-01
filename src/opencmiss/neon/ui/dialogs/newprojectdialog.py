"""
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
"""
from PySide import QtCore, QtGui

from opencmiss.neon.ui.dialogs.ui_newprojectdialog import Ui_NewProjectDialog


BIOMENG321 = True


class NewProjectDialog(QtGui.QDialog):

    openClicked = QtCore.Signal()
    recentClicked = QtCore.Signal([str])

    def __init__(self, project_model, parent):
        super(NewProjectDialog, self).__init__(parent)

        self._ui = Ui_NewProjectDialog()
        self._ui.setupUi(self)

        self._proxy_model = QtGui.QSortFilterProxyModel()
        self._proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self._setupProjects(project_model)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.toolButtonRecent.clicked.connect(self._recentClicked)
        if BIOMENG321:
            self._proxy_model.setFilterFixedString('Biomeng')
        else:
            self._ui.lineEditFilter.textChanged.connect(self._proxy_model.setFilterFixedString)

    def _setupProjects(self, model):
        self._proxy_model.setSourceModel(model)
        self._ui.listViewProjects.setModel(self._proxy_model)
        selection_model = self._ui.listViewProjects.selectionModel()
        selection_model.setCurrentIndex(self._proxy_model.index(0, 0), QtGui.QItemSelectionModel.Select)

    def setRecentActions(self, actions):
        self._ui.toolButtonRecent.addActions(actions)
        for action in actions:
            action.triggered.connect(self._recentActionTriggered)

    def _recentClicked(self):
        self._ui.toolButtonRecent.showMenu()

    def _recentActionTriggered(self):
        self.reject()

    def getSelectedIndex(self):
        selection_model = self._ui.listViewProjects.selectionModel()
        item_selection = self._proxy_model.mapSelectionToSource(selection_model.selection())
        indexes = item_selection.indexes()
        if len(indexes):
            return indexes[0]
