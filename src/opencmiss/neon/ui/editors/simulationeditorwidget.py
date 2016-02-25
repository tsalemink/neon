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

from opencmiss.neon.ui.editors.ui_simulationeditorwidget import Ui_SimulationEditorWidget


class SimulationEditorWidget(QtGui.QWidget):

    visualiseClicked = QtCore.Signal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._ui = Ui_SimulationEditorWidget()
        self._ui.setupUi(self)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.pushButtonVisualise.clicked.connect(self.visualiseClicked)
