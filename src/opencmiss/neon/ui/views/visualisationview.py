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

from PySide import QtCore, QtGui

from opencmiss.neon.ui.views.base import BaseView
from opencmiss.neon.ui.views.ui_visualisationview import Ui_VisualisationView


class VisualisationView(BaseView):

    graphicsInitialized = QtCore.Signal()

    def __init__(self, shared_opengl_widget, parent=None):
        super(VisualisationView, self).__init__(parent)
        self._name = 'Visualisation'

        self._ui = Ui_VisualisationView()
        self._ui.setupUi(shared_opengl_widget, self)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.widget.graphicsInitialized.connect(self.graphicsInitialized.emit)

    def setZincContext(self, zincContext):
        self._ui.widget.setContext(zincContext)

    def setScene(self, scene):
        self._ui.widget.getSceneviewer().setScene(scene)

    def setSceneviewerState(self, state):
        self._ui.widget.getSceneviewer().readDescription(json.dumps(state))

    def getSceneviewerState(self):
        d = json.loads(self._ui.widget.getSceneviewer().writeDescription())
        return d

    def saveImage(self, filename, wysiwyg, width, height):
        sv = self._ui.widget.getSceneviewer()
        if isinstance(filename, unicode):
            filename = str(filename)
        if wysiwyg:
            width = self._ui.widget.width()
            height = self._ui.widget.height()
        sv.writeImageToFile(filename, wysiwyg, width, height, 8, 0)

    def contextMenuEvent(self, event):
        if event.modifiers() & QtCore.Qt.CTRL:
            menu = QtGui.QMenu()
            menu.addAction("View All")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action:
                self._ui.widget.getSceneviewer().viewAll()
        else:
            event.ignore()

    def getShareGLWidget(self):
        return self._ui.widget

    def serialize(self):
        d = {}
        return json.dumps(d)

    def deserialize(self, string):
        pass
