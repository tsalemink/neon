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
from PySide import QtGui

from opencmiss.neon.ui.editors.ui_timeeditorwidget import Ui_TimeEditorWidget


class TimeEditorWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TimeEditorWidget, self).__init__(parent)
        self._ui = Ui_TimeEditorWidget()
        self._ui.setupUi(self)

        self._context = None

        self._makeConnections()

    def _makeConnections(self):
        pass

    def setContext(self, context):
        self._context = context
