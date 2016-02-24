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

from opencmiss.neon.ui.dialogs.ui_newproblemdialog import Ui_NewProblemDialog


class NewProblemDialog(QtGui.QDialog):

    openClicked = QtCore.Signal()
    recentClicked = QtCore.Signal([str])

    def __init__(self, model, parent):
        super(NewProblemDialog, self).__init__(parent)

        self._ui = Ui_NewProblemDialog()
        self._ui.setupUi(self)

        self._model = model

        self._makeConnections()

    def _makeConnections(self):
        self._ui.toolButtonRecent.clicked.connect(self._recentClicked)

    def setRecentActions(self, actions):
        self._ui.toolButtonRecent.addActions(actions)
        for action in actions:
            action.triggered.connect(self._recentActionTriggered)

    def _recentClicked(self):
        self._ui.toolButtonRecent.showMenu()

    def _recentActionTriggered(self):
        self.reject()

