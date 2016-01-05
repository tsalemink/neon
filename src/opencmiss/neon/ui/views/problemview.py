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
from PySide import QtCore, QtGui

from opencmiss.neon.ui.views.base import BaseView
from opencmiss.neon.ui.misc.factory import generateRelatedClasses

from opencmiss.neon.ui.views.ui_problemview import Ui_ProblemView
import json


class ProblemView(BaseView):

    runClicked = QtCore.Signal()
    selectionChanged = QtCore.Signal(object, object)

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
        self._ui.pushButtonRun.clicked.connect(self.runClicked)

    def _selectionChanged(self, current_index, previous_index):
        current_index = self._proxy_model.mapToSource(current_index)
        self._ui.stackedWidgetProblemView.setCurrentIndex(current_index.row())
        self.selectionChanged.emit(current_index, previous_index)

    def _setupProblems(self, model):
        classes = generateRelatedClasses(model, 'problems')
        for c in classes:
            c.setParent(self._ui.stackedWidgetProblemView)
            problem = model.getProblem(self._ui.stackedWidgetProblemView.count())
            c.setProblem(problem)
            self._ui.stackedWidgetProblemView.addWidget(c)

    def setContext(self, context):
        pass

    def setModel(self, model):
        self._proxy_model.setSourceModel(model)
        self._ui.listViewProblems.setModel(self._proxy_model)
        self._setupProblems(model)
        self._selection_model = self._ui.listViewProblems.selectionModel()
        self._selection_model.currentChanged.connect(self._selectionChanged)
        self._selection_model.setCurrentIndex(self._proxy_model.index(0, 0), QtGui.QItemSelectionModel.Select)

    def getProblem(self):
        index = self._ui.stackedWidgetProblemView.currentIndex()
        return self._proxy_model.sourceModel().getProblem(index)

    def serialise(self):
        state = {}
        state['current_index'] = self._ui.stackedWidgetProblemView.currentIndex()
        for index in range(self._ui.stackedWidgetProblemView.count()):
            w = self._ui.stackedWidgetProblemView.widget(index)
            state[w.getName()] = w.serialise()
        return json.dumps(state)

    def deserialise(self, string):
        try:
            d = json.loads(string)
            for index in range(self._ui.stackedWidgetProblemView.count()):
                w = self._ui.stackedWidgetProblemView.widget(index)
                w.deserialise(d[w.getName()])

            saved_current_index = d['current_index'] if 'current_index' in d else 0
            current_index = self._ui.stackedWidgetProblemView.currentIndex()
            if saved_current_index != current_index:
                self._selection_model.setCurrentIndex(self._proxy_model.index(saved_current_index, 0), QtGui.QItemSelectionModel.Select)
        except Exception:
            pass
