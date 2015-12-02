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

from opencmiss.neon.ui.views.ui_defaultview import Ui_DefaultView


class DefaultView(BaseView):

    graphicsInitialized = QtCore.Signal()

    def __init__(self, parent=None):
        super(DefaultView, self).__init__(parent)
        self._name = 'Default'

        self._ui = Ui_DefaultView()
        self._ui.setupUi(self)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.widget.graphicsInitialized.connect(self.graphicsInitialized.emit)

    def setContext(self, context):
        self._ui.widget.setContext(context)

    def getSceneviewer(self):
        return self._ui.widget.getSceneviewer()

    def saveImage(self, filename, wysiwyg, width, height):
        sv = self._ui.widget.getSceneviewer()
        sv.writeImageToFile(filename, wysiwyg, width, height, 0, 0)
