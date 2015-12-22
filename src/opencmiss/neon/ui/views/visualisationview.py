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

from opencmiss.neon.ui.views.base import BaseView
from opencmiss.neon.ui.editors.regioneditorwidget import RegionEditorWidget
from opencmiss.neon.ui.editors.sceneeditorwidget import SceneEditorWidget
from opencmiss.neon.ui.editors.spectrumeditorwidget import SpectrumEditorWidget
from opencmiss.neon.ui.editors.tessellationeditorwidget import TessellationEditorWidget
from opencmiss.neon.ui.editors.timeeditorwidget import TimeEditorWidget

from opencmiss.neon.ui.views.ui_visualisationview import Ui_VisualisationView


class VisualisationView(BaseView):

    graphicsInitialized = QtCore.Signal()
    regionClicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(VisualisationView, self).__init__(parent)
        self._name = 'Visualisation'

        self._ui = Ui_VisualisationView()
        self._ui.setupUi(self)

        self._setupEditors()

        self._makeConnections()

    def _makeConnections(self):
        self._ui.widget.graphicsInitialized.connect(self.graphicsInitialized.emit)
        self.dockWidgetContentsRegionEditor.regionSelected.connect(self.regionClicked)

    def _setupEditors(self):
        main_window = self.parent()
        self.dockWidgetRegionEditor = QtGui.QDockWidget(main_window)
        self.dockWidgetRegionEditor.setWindowTitle('Region Editor')
        self.dockWidgetRegionEditor.setObjectName("dockWidgetRegionEditor")
        self.dockWidgetContentsRegionEditor = RegionEditorWidget()
        self.dockWidgetContentsRegionEditor.setObjectName("dockWidgetContentsRegionEditor")
        self.dockWidgetRegionEditor.setWidget(self.dockWidgetContentsRegionEditor)

        self.dockWidgetSceneEditor = QtGui.QDockWidget(main_window)
        self.dockWidgetSceneEditor.setWindowTitle('Scene Editor')
        self.dockWidgetSceneEditor.setObjectName("dockWidgetSceneEditor")
        self.dockWidgetContentsSceneEditor = SceneEditorWidget()
        self.dockWidgetContentsSceneEditor.setObjectName("dockWidgetContentsSceneEditor")
        self.dockWidgetSceneEditor.setWidget(self.dockWidgetContentsSceneEditor)

        self.dockWidgetSpectrumEditor = QtGui.QDockWidget(main_window)
        self.dockWidgetSpectrumEditor.setWindowTitle('Spectrum Editor')
        self.dockWidgetSpectrumEditor.setObjectName("dockWidgetSpectrumEditor")
        self.dockWidgetContentsSpectrumEditor = SpectrumEditorWidget(self.dockWidgetSpectrumEditor, self._ui.widget)
        self.dockWidgetContentsSpectrumEditor.setObjectName("dockWidgetContentsSpectrumEditor")
        self.dockWidgetSpectrumEditor.setWidget(self.dockWidgetContentsSpectrumEditor)

        self.dockWidgetTessellationEditor = QtGui.QDockWidget(main_window)
        self.dockWidgetTessellationEditor.setWindowTitle('Tessellation Editor')
        self.dockWidgetTessellationEditor.setObjectName("dockWidgetTessellationEditor")
        self.dockWidgetContentsTessellationEditor = TessellationEditorWidget()
        self.dockWidgetContentsTessellationEditor.setObjectName("dockWidgetContentsTessellationEditor")
        self.dockWidgetTessellationEditor.setWidget(self.dockWidgetContentsTessellationEditor)

        self.dockWidgetTimeEditor = QtGui.QDockWidget(main_window)
        self.dockWidgetTimeEditor.setWindowTitle('Time Editor')
        self.dockWidgetTimeEditor.setObjectName("dockWidgetTimeEditor")
        self.dockWidgetContentsTimeEditor = TimeEditorWidget()
        self.dockWidgetContentsTimeEditor.setObjectName("dockWidgetContentsTimeEditor")
        self.dockWidgetTimeEditor.setWidget(self.dockWidgetContentsTimeEditor)
#         main_window.tabifyDockWidget(self.dockWidgetRegionEditor, self.dockWidgetTimeEditor)

        main_window.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetTessellationEditor)
        main_window.tabifyDockWidget(self.dockWidgetTessellationEditor, self.dockWidgetSpectrumEditor)
        main_window.tabifyDockWidget(self.dockWidgetSpectrumEditor, self.dockWidgetSceneEditor)
        main_window.tabifyDockWidget(self.dockWidgetSceneEditor, self.dockWidgetRegionEditor)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidgetTimeEditor)

        self._dependent_editors = [self.dockWidgetRegionEditor,
                                   self.dockWidgetSceneEditor,
                                   self.dockWidgetSpectrumEditor,
                                   self.dockWidgetTessellationEditor,
                                   self.dockWidgetTimeEditor]

    def setContext(self, context):
        self._ui.widget.setContext(context)
        self.dockWidgetContentsSpectrumEditor.setContext(context)
        self.dockWidgetContentsTessellationEditor.setContext(context)
        self.dockWidgetContentsTimeEditor.setContext(context)

    def setRootRegion(self, region):
        self.dockWidgetContentsRegionEditor.setRootRegion(region)

    def setScene(self, scene):
        self.dockWidgetContentsSceneEditor.setScene(scene)
        self.getSceneviewer().setScene(scene)

    def getSceneviewer(self):
        return self._ui.widget.getSceneviewer()

    def saveImage(self, filename, wysiwyg, width, height):
        sv = self._ui.widget.getSceneviewer()
        if isinstance(filename, unicode):
            filename = str(filename)
        if wysiwyg:
            width = self._ui.widget.width()
            height = self._ui.widget.height()
        sv.writeImageToFile(filename, wysiwyg, width, height, 8, 0)

    def getShareGLWidget(self):
        return self._ui.widget

    def getDependentEditors(self):
        return self._dependent_editors
