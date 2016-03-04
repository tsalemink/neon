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

from opencmiss.neon.ui.problems.base import BaseProblem
from opencmiss.neon.ui.problems.ui_biomeng321lab2 import Ui_Biomeng321Lab2
from opencmiss.neon.core.problems.biomeng321lab2 import BOUNDARY_CONDITIONS


class Biomeng321Lab2(BaseProblem):

    def __init__(self, shared_opengl_widget, parent=None):
        super(Biomeng321Lab2, self).__init__(parent)
        self._ui = Ui_Biomeng321Lab2()
        self._ui.setupUi(self)

        self._ui.comboBoxBoundaryConditions.clear()
        self._ui.comboBoxBoundaryConditions.addItems(BOUNDARY_CONDITIONS)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.comboBoxBoundaryConditions.currentIndexChanged.connect(self._boundaryConditionChanged)

    def _boundaryConditionChanged(self, index):
        self._problem.setBoundaryCondition(self._ui.comboBoxBoundaryConditions.currentText())

    def updateUi(self):
        boundary_condition = self._problem.getBoundaryCondition()
        if boundary_condition in BOUNDARY_CONDITIONS:
            index = BOUNDARY_CONDITIONS.index(boundary_condition)
            self._ui.comboBoxBoundaryConditions.setCurrentIndex(index)

    def serialize(self):
        d = {}
        d['problem'] = self._problem.serialize()

        return json.dumps(d)

    def deserialize(self, string):
        d = json.loads(string)
        if 'problem' in d:
            self._problem.deserialize(d['problem'])

        self.updateUi()
