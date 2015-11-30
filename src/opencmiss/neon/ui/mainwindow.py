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

from opencmiss.neon.ui.ui_mainwindow import Ui_MainWindow

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model
        
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        
        self._readSettings()
        
        self._makeConnections()
        
    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.quitApplication)
        
    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()
        
    def _readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self.resize(settings.value('size', QtCore.QSize(1200, 900)))
        self.move(settings.value('pos', QtCore.QPoint(100, 150)))
        settings.endGroup()
    
    def confirmClose(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.isModified():
            ret = QtGui.QMessageBox.warning(self, 'Unsaved Changes', 'You have unsaved changes, would you like to save these changes now?',
                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                self._model.save()

    
    def quitApplication(self):
        self.confirmClose()
        
        self._writeSettings()
        
        QtGui.qApp.quit()
        
        
        