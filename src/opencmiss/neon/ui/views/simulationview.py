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
from PySide import QtCore

from opencmiss.neon.ui.views.base import BaseView
from opencmiss.neon.ui.misc.factory import instantiateRelatedClasses

from opencmiss.neon.ui.views.ui_simulationview import Ui_SimulationView


class SimulationView(BaseView):

    def __init__(self, parent=None):
        super(SimulationView, self).__init__(parent)
        self._name = 'Simulation'

        self._ui = Ui_SimulationView()
        self._ui.setupUi(self)

        self._makeConnections()

    def _makeConnections(self):
        pass

    def setCurrentIndex(self, index):
        self._ui.stackedWidgetSimulationView.setCurrentIndex(index)

    def setupSimulations(self, model):
        swsv = self._ui.stackedWidgetSimulationView
        classes = instantiateRelatedClasses(model, 'simulations')
        for c in classes:
            c.setParent(swsv)
            project = model.getProject(model.index(swsv.count(), 0))
            c.setProblem(project.getProblem())
            swsv.addWidget(c)

    def setProblem(self, problem):
        widget = self._ui.stackedWidgetSimulationView.currentWidget()
        widget.setProblem(problem)

    def setPreferences(self, preferences):
        pass

    def getSimulation(self):
        widget = self._ui.stackedWidgetSimulationView.currentWidget()
        return widget.getSimulation()

    def setZincContext(self, zinc_context):
        pass

    def run(self):
        simulation = self._ui.stackedWidgetSimulationView.currentWidget()
        simulation.run()
