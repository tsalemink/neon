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
import importlib

from PySide import QtCore, QtGui

from opencmiss.neon.ui.views.base import BaseView

from opencmiss.neon.ui.views.ui_problemview import Ui_ProblemView


class ProblemView(BaseView):

    def __init__(self, parent=None):
        super(ProblemView, self).__init__(parent)
        self._name = 'Problem'

        self._ui = Ui_ProblemView()
        self._ui.setupUi(self)

        self._selection_model = None
        self._proxy_model = QtGui.QSortFilterProxyModel()
        self._proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.lineEditFilter.textChanged.connect(self._proxy_model.setFilterFixedString)

    def _selectionChanged(self, current_index, previous_index):
        current_index = self._proxy_model.mapToSource(current_index)
        self._ui.stackedWidgetProblemView.setCurrentIndex(current_index.row())

    def _setupProblems(self, model):
        for row in range(model.rowCount()):
            index = model.index(row)
            name = model.data(index, QtCore.Qt.DisplayRole)
            module_name = importlib.import_module('.' + name.lower(), 'opencmiss.neon.ui.problems')
            class_ = getattr(module_name, name)
            view = class_(self._ui.stackedWidgetProblemView)
            self._ui.stackedWidgetProblemView.addWidget(view)

    def setContext(self, context):
        pass

    def setModel(self, model):
        self._proxy_model.setSourceModel(model)
        self._ui.listViewProblems.setModel(self._proxy_model)
        self._setupProblems(model)
        self._selection_model = self._ui.listViewProblems.selectionModel()
        self._selection_model.currentChanged.connect(self._selectionChanged)
        self._selection_model.setCurrentIndex(self._proxy_model.index(0, 0), QtGui.QItemSelectionModel.Select)
