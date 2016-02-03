'''
   Copyright 2016 University of Auckland

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
from PySide import QtGui

import sys
from opencmiss.neon.ui.dialogs.ui_logger import Ui_Logger
from opencmiss.neon.core.neonlogger import CustomStream
    
class Logger(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._ui = Ui_Logger()
        self._ui.setupUi(self)
        
        self._logger = None
        self._loggerNotifier = None
        self._makeConnections()
        
    def writeMessage(self, message, levelstring):
        if levelstring == "ERROR":
            self._ui.logText.setTextColor(QtGui.QColor(255, 0, 0))
        elif levelstring == "WARNING":
            self._ui.logText.setTextColor(QtGui.QColor(255, 100, 0))
        elif levelstring == "INFORMATION":
            self._ui.logText.setTextColor(QtGui.QColor(0, 0, 0))
        self._ui.logText.insertPlainText(message)
        
    def _makeConnections(self):
        CustomStream.stdout().messageWritten.connect( self.writeMessage )
        CustomStream.stderr().messageWritten.connect( self.writeMessage )
        
    def copyToClipboard(self):
        QtGui.QApplication.clipboard().setText( self._ui.logText.toPlainText() )
        
    def clearAll(self):
        self._ui.logText.clear()
