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

    visualiseClicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(SimulationView, self).__init__(parent)
        self._name = 'Simulation'

        self._ui = Ui_SimulationView()
        self._ui.setupUi(self)

        self._run_delay_timer = QtCore.QTimer()
        self._run_delay_timer.setSingleShot(True)
        self._run_delay_timer.setInterval(10)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.pushButtonVisualise.clicked.connect(self.visualiseClicked)
        self._run_delay_timer.timeout.connect(self._run)

    def _setupSimulations(self, model):
        classes = instantiateRelatedClasses(model, 'simulations')
        for c in classes:
            c.setParent(self._ui.stackedWidgetSimulationView)
            self._ui.stackedWidgetSimulationView.addWidget(c)

    def selectionChanged(self, current_index, previous_index):
        self._ui.stackedWidgetSimulationView.setCurrentIndex(current_index.row())

    def setModel(self, model):
        self._setupSimulations(model)

    def setZincContext(self, zincContext):
        pass

    def setProblem(self, problem):
        simulation = self._ui.stackedWidgetSimulationView.currentWidget()
        simulation.setProblem(problem)

    def setPreferences(self, preferences):
        simulation = self._ui.stackedWidgetSimulationView.currentWidget()
        simulation.setPreferences(preferences)

    def run(self):
        self._run_delay_timer.start()

    def _run(self):
        simulation = self._ui.stackedWidgetSimulationView.currentWidget()
        simulation.run()

    def getSimulation(self):
        simulation_widget = self._ui.stackedWidgetSimulationView.currentWidget()
        return simulation_widget.getSimulation()
