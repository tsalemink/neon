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
import os.path

from PySide import QtCore, QtGui

from opencmiss.neon.ui.ui_mainwindow import Ui_MainWindow
from opencmiss.neon.undoredo.commands import CommandEmpty
from opencmiss.neon.ui.views.visualisationview import VisualisationView
from opencmiss.neon.ui.views.problemview import ProblemView
from opencmiss.neon.ui.views.simulationview import SimulationView
from opencmiss.neon.ui.dialogs.aboutdialog import AboutDialog
from opencmiss.neon.ui.dialogs.snapshotdialog import SnapshotDialog
from opencmiss.neon.ui.dialogs.preferencesdialog import PreferencesDialog
from opencmiss.neon.ui.editors.regioneditorwidget import RegionEditorWidget
from opencmiss.neon.ui.editors.modelsourceseditorwidget import ModelSourcesEditorWidget
from opencmiss.neon.ui.editors.sceneeditorwidget import SceneEditorWidget
from opencmiss.neon.ui.editors.spectrumeditorwidget import SpectrumEditorWidget
from opencmiss.neon.ui.editors.tessellationeditorwidget import TessellationEditorWidget
from opencmiss.neon.ui.editors.timeeditorwidget import TimeEditorWidget
from opencmiss.neon.settings.mainsettings import VERSION_MAJOR


class MainWindow(QtGui.QMainWindow):

    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model
        problem_model = self._model.getProblemModel()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # List of possible views
        self._visualisation_view = VisualisationView(self)
        self._visualisation_view_ready = False
        self._problem_view = ProblemView(self)
        self._problem_view.setModel(problem_model)
        self._simulation_view = SimulationView(self)
        self._simulation_view.setModel(problem_model)

        self._view_states = {}
        self._view_states[self._visualisation_view] = ''
        self._view_states[self._problem_view] = ''
        self._view_states[self._simulation_view] = ''

        view_list = [self._problem_view, self._simulation_view, self._visualisation_view]
        self._shared_gl_widget = self._visualisation_view.getShareGLWidget()

        self._location = None  # The last location/directory used by the application
        self._current_view = None

        self._undoRedoStack = QtGui.QUndoStack(self)

        # Pre-create dialogs
        self._createDialogs()

        self._setupEditors()

        self._registerEditors()

        self._setupViews(view_list)

        self._makeConnections()

        # Set the undo redo stack state
        self._undoRedoStack.push(CommandEmpty())
        self._undoRedoStack.clear()

        self._updateUi()

        self._readSettings()
#         QtCore.QTimer.singleShot(0, self._readSettings)

    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.close)
        self._ui.action_New.triggered.connect(self._newTriggered)
        self._ui.action_Open.triggered.connect(self._openTriggered)
        self._ui.action_About.triggered.connect(self._aboutTriggered)
        self._ui.action_Save.triggered.connect(self._saveTriggered)
        self._ui.action_Save_As.triggered.connect(self._saveAsTriggered)
        self._ui.action_Snapshot.triggered.connect(self._snapshotTriggered)
        self._ui.actionPreferences.triggered.connect(self._preferencesTriggered)
        self._ui.action_Clear.triggered.connect(self._clearTriggered)

        self._undoRedoStack.indexChanged.connect(self._undoRedoStackIndexChanged)
        self._undoRedoStack.canUndoChanged.connect(self._ui.action_Undo.setEnabled)
        self._undoRedoStack.canRedoChanged.connect(self._ui.action_Redo.setEnabled)

        self._visualisation_view.graphicsInitialized.connect(self._visualisationViewReady)

        self._snapshot_dialog.sceneviewerInitialized.connect(self._snapshotDialogReady)

        self.dockWidgetContentsRegionEditor.regionSelected.connect(self._regionSelected)

        self._problem_view.runClicked.connect(self._runSimulationClicked)
        self._problem_view.selectionChanged.connect(self._simulation_view.selectionChanged)
        self._simulation_view.runClicked.connect(self._runSimulationClicked)

    def _updateUi(self):
        modified = self._model.isModified()
        self._ui.action_Save.setEnabled(modified)
        recents = self._model.getRecents()
        self._ui.action_Clear.setEnabled(len(recents))

    def _setupEditors(self):
        self.dockWidgetRegionEditor = QtGui.QDockWidget(self)
        self.dockWidgetRegionEditor.setWindowTitle('Region Editor')
        self.dockWidgetRegionEditor.setObjectName("dockWidgetRegionEditor")
        self.dockWidgetContentsRegionEditor = RegionEditorWidget()
        self.dockWidgetContentsRegionEditor.setObjectName("dockWidgetContentsRegionEditor")
        self.dockWidgetRegionEditor.setWidget(self.dockWidgetContentsRegionEditor)
        self.dockWidgetRegionEditor.setHidden(True)

        self.dockWidgetModelSourcesEditor = QtGui.QDockWidget(self)
        self.dockWidgetModelSourcesEditor.setWindowTitle('Model Sources Editor')
        self.dockWidgetModelSourcesEditor.setObjectName("dockWidgetModelSourcesEditor")
        self.dockWidgetContentsModelSourcesEditor = ModelSourcesEditorWidget()
        self.dockWidgetContentsModelSourcesEditor.setObjectName("dockWidgetContentsModelSourcesEditor")
        self.dockWidgetModelSourcesEditor.setWidget(self.dockWidgetContentsModelSourcesEditor)
        self.dockWidgetModelSourcesEditor.setHidden(True)

        self.dockWidgetSceneEditor = QtGui.QDockWidget(self)
        self.dockWidgetSceneEditor.setWindowTitle('Scene Editor')
        self.dockWidgetSceneEditor.setObjectName("dockWidgetSceneEditor")
        self.dockWidgetContentsSceneEditor = SceneEditorWidget()
        self.dockWidgetContentsSceneEditor.setObjectName("dockWidgetContentsSceneEditor")
        self.dockWidgetSceneEditor.setWidget(self.dockWidgetContentsSceneEditor)
        self.dockWidgetSceneEditor.setHidden(True)

        self.dockWidgetSpectrumEditor = QtGui.QDockWidget(self)
        self.dockWidgetSpectrumEditor.setWindowTitle('Spectrum Editor')
        self.dockWidgetSpectrumEditor.setObjectName("dockWidgetSpectrumEditor")
        self.dockWidgetContentsSpectrumEditor = SpectrumEditorWidget(self.dockWidgetSpectrumEditor, self._shared_gl_widget)
        self.dockWidgetContentsSpectrumEditor.setObjectName("dockWidgetContentsSpectrumEditor")
        self.dockWidgetSpectrumEditor.setWidget(self.dockWidgetContentsSpectrumEditor)
        self.dockWidgetSpectrumEditor.setHidden(True)

        self.dockWidgetTessellationEditor = QtGui.QDockWidget(self)
        self.dockWidgetTessellationEditor.setWindowTitle('Tessellation Editor')
        self.dockWidgetTessellationEditor.setObjectName("dockWidgetTessellationEditor")
        self.dockWidgetContentsTessellationEditor = TessellationEditorWidget()
        self.dockWidgetContentsTessellationEditor.setObjectName("dockWidgetContentsTessellationEditor")
        self.dockWidgetTessellationEditor.setWidget(self.dockWidgetContentsTessellationEditor)
        self.dockWidgetTessellationEditor.setHidden(True)

        self.dockWidgetTimeEditor = QtGui.QDockWidget(self)
        self.dockWidgetTimeEditor.setWindowTitle('Time Editor')
        self.dockWidgetTimeEditor.setObjectName("dockWidgetTimeEditor")
        self.dockWidgetContentsTimeEditor = TimeEditorWidget()
        self.dockWidgetContentsTimeEditor.setObjectName("dockWidgetContentsTimeEditor")
        self.dockWidgetTimeEditor.setWidget(self.dockWidgetContentsTimeEditor)
        self.dockWidgetTimeEditor.setHidden(True)

        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetTessellationEditor)
        self.tabifyDockWidget(self.dockWidgetTessellationEditor, self.dockWidgetSpectrumEditor)
        self.tabifyDockWidget(self.dockWidgetSpectrumEditor, self.dockWidgetSceneEditor)
        self.tabifyDockWidget(self.dockWidgetSceneEditor, self.dockWidgetModelSourcesEditor)
        self.tabifyDockWidget(self.dockWidgetModelSourcesEditor, self.dockWidgetRegionEditor)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidgetTimeEditor)

        zincContext = self._model.getZincContext()
        self.dockWidgetContentsSpectrumEditor.setZincContext(zincContext)
        self.dockWidgetContentsTessellationEditor.setZincContext(zincContext)
        self.dockWidgetContentsTimeEditor.setZincContext(zincContext)

    def _registerEditors(self):
        self._registerEditor(self._visualisation_view, self.dockWidgetRegionEditor)
        self._registerEditor(self._visualisation_view, self.dockWidgetModelSourcesEditor)
        self._registerEditor(self._visualisation_view, self.dockWidgetSceneEditor)
        self._registerEditor(self._visualisation_view, self.dockWidgetSpectrumEditor)
        self._registerEditor(self._visualisation_view, self.dockWidgetTessellationEditor)
        self._registerEditor(self._visualisation_view, self.dockWidgetTimeEditor)

        self._ui.menu_View.addSeparator()

    def _registerEditor(self, view, editor):
        action_name = getEditorMenuName(view)
        action = self._getEditorAction(action_name)
        if action is None:
            menu = self._ui.menu_View.addMenu(action_name)
            menu.setEnabled(False)
        else:
            menu = action.menu()

        menu.addAction(editor.toggleViewAction())
        view.registerDependentEditor(editor)

    def _getEditorAction(self, action_name):
        action = None
        actions = self._ui.menu_View.actions()
        existing_actions = [a for a in actions if a.text() == action_name]
        if existing_actions:
            action = existing_actions[0]

        return action

    def _createDialogs(self):
        self._snapshot_dialog = SnapshotDialog(self, self._shared_gl_widget)
        self._snapshot_dialog.setZincContext(self._model.getZincContext())

        self._preferences_dialog = PreferencesDialog(self)

    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('location', self._location)
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('dock_locations', self.saveState(VERSION_MAJOR))
        settings.setValue('current_view', self._ui.viewStackedWidget.currentIndex())

        settings.beginWriteArray('recents')
        recents = self._model.getRecents()
        for i, r in enumerate(recents):
            settings.setArrayIndex(i)
            settings.setValue('item', r)
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('views')
        for key in self._view_states:
            settings.setValue(key.getName(), self._view_states[key])
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        settings.setValue('state', self._snapshot_dialog.serialise())
        settings.endGroup()

        settings.beginGroup('Problems')
        settings.setValue('state', self._problem_view.serialise())
        settings.endGroup()

    def _readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        geometry = settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        state = settings.value('dock_locations')
        if state is not None:
            self.restoreState(state, VERSION_MAJOR)
        self._location = settings.value('location', QtCore.QDir.homePath())

        size = settings.beginReadArray('recents')
        for i in range(size):
            settings.setArrayIndex(i)
            self._addRecent(settings.value('item'))
        settings.endArray()
        self._setCurrentView(settings.value('current_view', '0'))
        settings.endGroup()

        settings.beginGroup('views')
        for key in self._view_states:
            state = settings.value(key.getName(), '')
            self._view_states[key] = state
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        self._snapshot_dialog.deserialise(settings.value('state', ''))
        settings.endGroup()

        settings.beginGroup('Problems')
        self._problem_view.deserialise(settings.value('state', ''))
        settings.endGroup()

        self._updateUi()

    def _addRecent(self, recent):
        actions = self._ui.menu_Open_recent.actions()
        insert_before_action = actions[0]
        self._model.addRecent(recent)
        recent_action = QtGui.QAction(self._ui.menu_Open_recent)
        recent_action.setText(recent)
        self._ui.menu_Open_recent.insertAction(insert_before_action, recent_action)
        recent_action.triggered.connect(self._open)

    def _setCurrentView(self, index):
        v = self._ui.viewStackedWidget.widget(int(index))
        self._changeView(v)
        self._postChangeView()
        actions = self._ui.menu_View.actions()
        for action in actions:
            if action.data() == v:
                action.setChecked(True)

    def _preChangeView(self):
        current_view = self._ui.viewStackedWidget.currentWidget()
        view_state = self.saveState(VERSION_MAJOR)
        self._view_states[current_view] = view_state

        action_name = getEditorMenuName(current_view)
        action = self._getEditorAction(action_name)
        if action is not None:
            menu = action.menu()
            menu.setEnabled(False)

    def _changeView(self, view):
        self._ui.viewStackedWidget.setCurrentWidget(view)

    def _postChangeView(self):
        current_view = self._ui.viewStackedWidget.currentWidget()
        view_state = self._view_states[current_view]
        self.restoreState(view_state, VERSION_MAJOR)

        action_name = getEditorMenuName(current_view)
        action = self._getEditorAction(action_name)
        if action is not None:
            menu = action.menu()
            menu.setEnabled(True)

    def _setupViews(self, views):
        action_group = QtGui.QActionGroup(self)
        zincContext = self._model.getZincContext()
        for v in views:
            self._ui.viewStackedWidget.addWidget(v)
            v.setZincContext(zincContext)

            action_view = QtGui.QAction(v.getName(), self)
            action_view.setData(v)
            action_view.setCheckable(True)
            action_view.setActionGroup(action_group)
            action_view.triggered.connect(self._viewTriggered)
            self._ui.menu_View.addAction(action_view)

    def _runSimulationClicked(self):
        sender = self.sender()
        if sender == self._problem_view:
            actions = self._ui.menu_View.actions()
            simulate_action = [a for a in actions if a.text() == self._simulation_view.getName()][0]
            simulate_action.activate(QtGui.QAction.ActionEvent.Trigger)

        problem = self._problem_view.getProblem()
        if problem.validate():
            self._simulation_view.setProblem(problem)
            self._simulation_view.setPreferences(self._model.getPreferences())
            self._simulation_view.run()
        else:
            print('pop up error box')

    def _viewTriggered(self):
        v = self.sender().data()
        self._preChangeView()
        self._changeView(v)
        self._postChangeView()

    def _regionChange(self, changedRegion, treeChange):
        """
        Notifies sceneviewer if affected by tree change i.e. needs new scene.
        :param changedRegion: The top region changed
        :param treeChange: True if structure of tree, or zinc objects reconstructed
        """
        # following may need changing once sceneviewer can look at sub scenes, since resets to root scene:
        if treeChange and (changedRegion is self._model.getDocument().getRootRegion()):
            zincRootRegion = changedRegion.getZincRegion()
            self._visualisation_view.setScene(zincRootRegion.getScene())

    def _onNewDocument(self):
        document = self._model.getDocument()
        rootRegion = document.getRootRegion()
        rootRegion.connectRegionChange(self._regionChange)

        # need to pass new Zinc context to dialogs and widgets using global modules
        zincContext = document.getZincContext()
        self._visualisation_view.setZincContext(zincContext)
        self.dockWidgetContentsSpectrumEditor.setZincContext(zincContext)
        self.dockWidgetContentsTessellationEditor.setZincContext(zincContext)
        self.dockWidgetContentsTimeEditor.setZincContext(zincContext)
        self._snapshot_dialog.setZincContext(zincContext)

        # need to pass new root region to the following
        self.dockWidgetContentsRegionEditor.setRootRegion(rootRegion)
        self.dockWidgetContentsModelSourcesEditor.setRegion(rootRegion)

        # need to pass new scene to the following
        zincRootRegion = rootRegion.getZincRegion()
        scene = zincRootRegion.getScene()
        self.dockWidgetContentsSceneEditor.setScene(scene)

    def _regionSelected(self, region):
        self.dockWidgetContentsModelSourcesEditor.setRegion(region)
        zincRegion = region.getZincRegion()
        scene = zincRegion.getScene()
        self.dockWidgetContentsSceneEditor.setScene(scene)

    def _visualisationViewReady(self):
        self._visualisation_view_ready = True
        self._onNewDocument()

    def _saveTriggered(self):
        if self._model.getLocation() is None:
            self._saveAsTriggered()
        else:
            self._model.save()

    def _saveAsTriggered(self):
        filename, _ = QtGui.QFileDialog.getSaveFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")
        if filename:
            self._location = os.path.dirname(filename)
            self._model.setLocation(filename)
            self._model.save()

    def _undoRedoStackIndexChanged(self, index):
        self._model.setCurrentUndoRedoIndex(index)

    def _aboutTriggered(self):
        d = AboutDialog(self)
        d.exec_()

    def _snapshotDialogReady(self):
        document = self._model.getDocument()
        rootRegion = document.getRootRegion()
        zincRootRegion = rootRegion.getZincRegion()
        scene = zincRootRegion.getScene()
        self._snapshot_dialog.setScene(scene)

    def _snapshotTriggered(self):
        if self._snapshot_dialog.getLocation() is None and self._location is not None:
            self._snapshot_dialog.setLocation(self._location)

        if self._snapshot_dialog.exec_():
            if self._location is None:
                self._location = self._snapshot_dialog.getLocation()
            filename = self._snapshot_dialog.getFilename()
            wysiwyg = self._snapshot_dialog.getWYSIWYG()
            width = self._snapshot_dialog.getWidth()
            height = self._snapshot_dialog.getHeight()
            self._visualisation_view.saveImage(filename, wysiwyg, width, height)

    def _preferencesTriggered(self):
        if self._preferences_dialog.exec_():
            pass  # Save the state

    def _newTriggered(self):
        self._model.new()
        self._onNewDocument()

    def _openModel(self, filename):
        self._location = os.path.dirname(filename)
        self._model.load(filename)
        self._addRecent(filename)
        self._onNewDocument()

        self._updateUi()

    def _openTriggered(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")

        if filename:
            self._openModel(filename)

    def _open(self):
        '''
        Open a model from a recent file
        '''
        filename = self.sender().text()
        self._ui.menu_Open_recent.removeAction(self.sender())
        self._openModel(filename)

    def _clearTriggered(self):
        self._model.clearRecents()
        actions = self._ui.menu_Open_recent.actions()
        for action in actions[:-2]:
            self._ui.menu_Open_recent.removeAction(action)

        self._updateUi()

    def confirmClose(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.isModified():
            ret = QtGui.QMessageBox.warning(self, 'Unsaved Changes', 'You have unsaved changes, would you like to save these changes now?',
                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                self._saveTriggered()

    def _quitApplication(self):
        self.confirmClose()
        self._writeSettings()

    def closeEvent(self, event):
        self._quitApplication()
        super(MainWindow, self).closeEvent(event)


def getEditorMenuName(view):
    return view.getName() + ' Editors'
