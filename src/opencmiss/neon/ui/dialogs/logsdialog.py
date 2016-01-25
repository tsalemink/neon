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

from opencmiss.neon.ui.dialogs.ui_logsdialog import Ui_LogsDialog
from opencmiss.zinc.logger import Logger

class LogsDialog(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._ui = Ui_LogsDialog()
        self._ui.setupUi(self)
        
        self._logger = None
        self._loggerNotifier = None
        
        self._makeConnections()
        
    def _makeConnections(self):
        self._ui.clearAllButton.clicked.connect(self.clearAll)
        
    def clearAll(self):
        self._ui.logText.clear()
        
    def writeErrorMessage(self, string):
        self._ui.logText.setTextColor(QtGui.QColor(255, 0, 0))
        self._ui.logText.append('Error: ' + string)
        
    def writeWarningMessage(self, string):
        self._ui.logText.setTextColor(QtGui.QColor(255, 100, 0))
        self._ui.logText.append('Warning: ' + string)
        
    def writeInformationMessage(self, string):
        self._ui.logText.setTextColor(QtGui.QColor(0, 0, 0))
        self._ui.logText.append('Information: ' + string)
        
    def loggerCallback(self, event):
        if event.getChangeFlags() == Logger.CHANGE_FLAG_NEW_MESSAGE:
            if event.getMessageType() == Logger.MESSAGE_TYPE_ERROR:
                self.writeErrorMessage(event.getMessageText())

    def setZincContext(self, zincContext):
        self._logger = zincContext.getLogger()
        self._loggerNotifier = self._logger.createLoggernotifier()
        self._loggerNotifier.setCallback(self.loggerCallback)
        
