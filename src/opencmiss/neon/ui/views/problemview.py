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
import json

from PySide import QtCore

from opencmiss.neon.ui.views.base import BaseView
from opencmiss.neon.ui.views.ui_problemview import Ui_ProblemView
from opencmiss.neon.ui.misc.factory import instantiateRelatedClasses


BIOMENG321 = False


class ProblemView(BaseView):

    runClicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(ProblemView, self).__init__(parent)
        self._name = 'Problem View'

        self._ui = Ui_ProblemView()
        self._ui.setupUi(self)

        self._makeConnections()

    def _makeConnections(self):
        pass

    def setZincContext(self, zinc_context):
        pass

    def setupProblems(self, model):
        classes = instantiateRelatedClasses(model, 'problems')
        for c in classes:
            c.setParent(self._ui.stackedWidgetProblemView)
            project = model.getProject(model.index(self._ui.stackedWidgetProblemView.count(), 0))
            c.setProblem(project.getProblem())
            self._ui.stackedWidgetProblemView.addWidget(c)

    def setCurrentIndex(self, index):
        self._ui.stackedWidgetProblemView.setCurrentIndex(index)

    def setProblem(self, problem):
        widget = self._ui.stackedWidgetProblemView.currentWidget()
        widget.setProblem(problem)

    def getProblem(self):
        widget = self._ui.stackedWidgetProblemView.currentWidget()
        return widget.getProblem()

    def serialize(self):
        state = {}
        for index in range(self._ui.stackedWidgetProblemView.count()):
            w = self._ui.stackedWidgetProblemView.widget(index)
            state[w.getName()] = w.serialize()

        return json.dumps(state)

    def deserialize(self, string):
        try:
            d = json.loads(string)
            for index in range(self._ui.stackedWidgetProblemView.count()):
                w = self._ui.stackedWidgetProblemView.widget(index)
                w.deserialize(d[w.getName()])

        except Exception:
            pass
