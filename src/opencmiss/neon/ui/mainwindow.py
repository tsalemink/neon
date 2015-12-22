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


class MainWindow(QtGui.QMainWindow):

    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        # List of possible views
        self._view_states = {}
        self._visualisation_view = VisualisationView(self)
        self._visualisation_view_ready = False
        self._problem_view = ProblemView(self)
        self._problem_view.setModel(self._model.getProblemModel())
        self._simulation_view = SimulationView(self)
        view_list = [self._problem_view, self._simulation_view, self._visualisation_view]
        self._shared_gl_widget = self._visualisation_view.getShareGLWidget()

        self._location = None  # The last location/directory used by the application
        self._current_view = None

        self._undoRedoStack = QtGui.QUndoStack(self)

        # Pre-create dialogs
        self._createDialogs()

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
        self._visualisation_view.regionClicked.connect(self._regionSelected)

        self._snapshot_dialog.sceneviewerInitialized.connect(self._snapshotDialogReady)

    def _updateUi(self):
        modified = self._model.isModified()
        self._ui.action_Save.setEnabled(modified)
        recents = self._model.getRecents()
        self._ui.action_Clear.setEnabled(len(recents))

    def _createDialogs(self):
        self._snapshot_dialog = SnapshotDialog(self, self._shared_gl_widget)
        self._snapshot_dialog.setContext(self._model.getContext())

        self._preferences_dialog = PreferencesDialog(self)

    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('location', self._location)
        # settings.setValue('geometry', self.saveGeometry())
        # settings.setValue('dock_locations', self.saveState(VERSION_MAJOR))
        settings.setValue('current_view', self._ui.viewStackedWidget.currentIndex())

        settings.beginWriteArray('recents')
        recents = self._model.getRecents()
        for i, r in enumerate(recents):
            settings.setArrayIndex(i)
            settings.setValue('item', r)
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        settings.setValue('state', self._snapshot_dialog.serialise())
        settings.endGroup()

    def _readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        # geometry = settings.value('geometry')
        # if geometry is not None:
        #    self.restoreGeometry(geometry)
        # state = settings.value('dock_locations')
        # if state is not None:
        #    self.restoreState(state, VERSION_MAJOR)
        self._location = settings.value('location', QtCore.QDir.homePath())

        size = settings.beginReadArray('recents')
        for i in range(size):
            settings.setArrayIndex(i)
            self._addRecent(settings.value('item'))
        settings.endArray()
        self._setCurrentView(settings.value('current_view', '0'))
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        self._snapshot_dialog.deserialise(settings.value('state', ''))
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
        self._ui.viewStackedWidget.setCurrentIndex(int(index))
        v = self._ui.viewStackedWidget.currentWidget()
        actions = self._ui.menu_View.actions()
        for action in actions:
            if action.data() == v:
                action.setChecked(True)

    def _preChangeView(self):
        current_view = self._ui.viewStackedWidget.currentWidget()
        view_state = current_view.serialise()
        self._view_states[current_view] = view_state

    def _changeView(self, view):
        self._ui.viewStackedWidget.setCurrentWidget(view)

    def _postChangeView(self):
        current_view = self._ui.viewStackedWidget.currentWidget()
        view_state = self._view_states[current_view]
        current_view.deserialise(view_state)

    def _setupViews(self, views):
        action_group = QtGui.QActionGroup(self)
        context = self._model.getContext()
        for v in views:
            self._ui.viewStackedWidget.addWidget(v)
            v.setContext(context)

            action_view = QtGui.QAction(v.name(), self)
            action_view.setData(v)
            action_view.setCheckable(True)
            action_view.setActionGroup(action_group)
            action_view.triggered.connect(self._viewTriggered)
            self._ui.menu_View.addAction(action_view)

    def _viewTriggered(self):
        v = self.sender().data()
        self._preChangeView()
        self._changeView(v)
        self._postChangeView()

    def _refreshRootRegion(self):
        document = self._model.getDocument()
        rootRegion = document.getRootRegion()
        self._visualisation_view.setRootRegion(rootRegion)
        if self._visualisation_view_ready:
            zincRootRegion = rootRegion.getZincRegion()
            scene = zincRootRegion.getScene()
            self._visualisation_view.setScene(scene)

    def _regionSelected(self, region):
        zincRegion = region.getZincRegion()
        scene = zincRegion.getScene()
        self._ui.dockWidgetContentsSceneEditor.setScene(scene)

    def _visualisationViewReady(self):
        self._visualisation_view_ready = True
        self._refreshRootRegion()

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
        self._refreshRootRegion()

    def _openModel(self, filename):
        self._location = os.path.dirname(filename)
        self._model.load(filename)
        self._addRecent(filename)
        self._refreshRootRegion()

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
