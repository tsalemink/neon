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
from opencmiss.neon.settings.mainsettings import VERSION_MAJOR
from opencmiss.neon.ui.dialogs.aboutdialog import AboutDialog
from opencmiss.neon.ui.dialogs.snapshotdialog import SnapshotDialog


class MainWindow(QtGui.QMainWindow):

    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model

        # List of possible views
        view_list = [VisualisationView(self)]
        self._shared_gl_widget = view_list[0].getShareGLWidget()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self, self._shared_gl_widget)

        self._ui.menu_View.addAction(self._ui.dockWidgetRegionEditor.toggleViewAction())
        self._ui.menu_View.addAction(self._ui.dockWidgetSceneEditor.toggleViewAction())
        self._ui.menu_View.addAction(self._ui.dockWidgetSpectrumEditor.toggleViewAction())
        self._ui.menu_View.addAction(self._ui.dockWidgetTessellationEditor.toggleViewAction())
        self._ui.menu_View.addAction(self._ui.dockWidgetTimeEditor.toggleViewAction())
        self._ui.menu_View.addSeparator()

        self._location = None  # The last location/directory used by the application
        self._current_view = None

        self._undoRedoStack = QtGui.QUndoStack(self)

        self._shareContext()

        # Pre-create dialogs
        self._createDialogs()

        self._setupViews(view_list)

        self._makeConnections()

        # Set the undo redo stack state
        self._undoRedoStack.push(CommandEmpty())
        self._undoRedoStack.clear()

        self._updateUi()

        QtCore.QTimer.singleShot(0, self._readSettings)

    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.close)
        self._ui.action_New.triggered.connect(self._newTriggered)
        self._ui.action_Open.triggered.connect(self._openTriggered)
        self._ui.action_About.triggered.connect(self._aboutTriggered)
        self._ui.action_Save.triggered.connect(self._saveTriggered)
        self._ui.action_Save_As.triggered.connect(self._saveAsTriggered)
        self._ui.action_Snapshot.triggered.connect(self._snapshotTriggered)
        self._ui.action_Clear.triggered.connect(self._clearTriggered)

        self._undoRedoStack.indexChanged.connect(self._undoRedoStackIndexChanged)
        self._undoRedoStack.canUndoChanged.connect(self._ui.action_Undo.setEnabled)
        self._undoRedoStack.canRedoChanged.connect(self._ui.action_Redo.setEnabled)

        self._current_view.graphicsInitialized.connect(self._viewReady)
        self._ui.dockWidgetContentsRegionEditor.regionSelected.connect(self._regionSelected)

    def _updateUi(self):
        modified = self._model.isModified()
        self._ui.action_Save.setEnabled(modified)
        recents = self._model.getRecents()
        self._ui.action_Clear.setEnabled(len(recents))

    def _createDialogs(self):
        self._snapshotDialog = SnapshotDialog(self, self._shared_gl_widget)
        self._snapshotDialog.setContext(self._model.getContext())

    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('location', self._location)
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('dock_locations', self.saveState(VERSION_MAJOR))
        settings.setValue('sceneeditor_visibility', self._ui.action_SceneEditor.isChecked())
        settings.setValue('spectrumeditor_visibility', self._ui.action_SpectrumEditor.isChecked())

        settings.beginWriteArray('recents')
        recents = self._model.getRecents()
        for i, r in enumerate(recents):
            settings.setArrayIndex(i)
            settings.setValue('item', r)
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        settings.setValue('state', self._snapshotDialog.serialise())
        settings.endGroup()

    def _readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        state = settings.value('dock_locations')
        if state is not None:
            self.restoreState(state, VERSION_MAJOR)
        geometry = settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)

        self._location = settings.value('location', QtCore.QDir.homePath())

        self._ui.action_SceneEditor.setChecked(settings.value('sceneeditor_visibility', 'true') == 'true')
        self._ui.action_SpectrumEditor.setChecked(settings.value('spectrumeditor_visibility', 'true') == 'true')
        size = settings.beginReadArray('recents')
        for i in range(size):
            settings.setArrayIndex(i)
            self._addRecent(settings.value('item'))
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        self._snapshotDialog.deserialise(settings.value('state', ''))
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

    def _shareContext(self):
        context = self._model.getContext()
        self._ui.dockWidgetContentsSpectrumEditor.setContext(context)
        self._ui.dockWidgetContentsTessellationEditor.setContext(context)
        self._ui.dockWidgetContentsTimeEditor.setContext(context)

    def _setupViews(self, views):
        action_group = QtGui.QActionGroup(self)
        context = self._model.getContext()
        for v in views:
            self._ui.viewStackedWidget.addWidget(v)
            v.setContext(context)

            action_view = QtGui.QAction(v.name(), self)
            action_view.setCheckable(True)
            action_view.setChecked(True)
            action_view.setActionGroup(action_group)
            self._ui.menu_View.addAction(action_view)
            self._current_view = v

    def _refreshRootRegion(self):
        document = self._model.getDocument()
        rootRegion = document.getRootRegion()
        self._ui.dockWidgetContentsRegionEditor.setRootRegion(rootRegion)
        zincRootRegion = rootRegion.getZincRegion()
        scene = zincRootRegion.getScene()
        self._ui.dockWidgetContentsSceneEditor.setScene(scene)
        self._current_view.getSceneviewer().setScene(scene)

    def _regionSelected(self, region):
        zincRegion = region.getZincRegion()
        scene = zincRegion.getScene()
        self._ui.dockWidgetContentsSceneEditor.setScene(scene)

    def _viewReady(self):
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

    def _snapshotTriggered(self):
        if self._snapshotDialog.getLocation() is None and self._location is not None:
            self._snapshotDialog.setLocation(self._location)
        if self._snapshotDialog.exec_():
            if self._location is None:
                self._location = self._snapshotDialog.getLocation()
            filename = self._snapshotDialog.getFilename()
            wysiwyg = self._snapshotDialog.getWYSIWYG()
            width = self._snapshotDialog.getWidth()
            height = self._snapshotDialog.getHeight()
            self._current_view.saveImage(filename, wysiwyg, width, height)

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
