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
from opencmiss.neon.ui.views.defaultview import DefaultView
from opencmiss.neon.settings.mainsettings import VERSION_MAJOR
from opencmiss.neon.ui.dialogs.aboutdialog import AboutDialog
from opencmiss.neon.ui.dialogs.snapshotdialog import SnapshotDialog


class MainWindow(QtGui.QMainWindow):

    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._location = None  # The last location/directory used by the application
        self._current_view = None

        self._undoRedoStack = QtGui.QUndoStack(self)

        # Pre-create dialogs
        self._createDialogs()

        self._readSettings()

        self._actionDockWidgetMap = {self._ui.action_SceneEditor: self._ui.dockWidgetSceneEditor, self._ui.dockWidgetSceneEditor: self._ui.action_SceneEditor}

        # List of possible views
        view_list = [DefaultView(self)]
        self._setupViews(view_list)

        self._makeConnections()

        # Set the undo redo stack state
        self._undoRedoStack.push(CommandEmpty())
        self._undoRedoStack.clear()

    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.quitApplication)
        self._ui.action_Open.triggered.connect(self._openTriggered)
        self._ui.action_About.triggered.connect(self._aboutTriggered)
        self._ui.action_Save.triggered.connect(self._saveTriggered)
        self._ui.action_Save_As.triggered.connect(self._saveAsTriggered)
        self._ui.action_Snapshot.triggered.connect(self._snapshotTriggered)

        self._ui.action_SceneEditor.triggered.connect(self._dockWidgetTriggered)
        self._ui.dockWidgetSceneEditor.visibilityChanged.connect(self._dockWidgetVisibilityChanged)

        self._undoRedoStack.indexChanged.connect(self._undoRedoStackIndexChanged)
        self._undoRedoStack.canUndoChanged.connect(self._ui.action_Undo.setEnabled)
        self._undoRedoStack.canRedoChanged.connect(self._ui.action_Redo.setEnabled)

        self._current_view.graphicsInitialized.connect(self._viewReady)

    def _createDialogs(self):
        self._snapshotDialog = SnapshotDialog(self)

    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.setValue('location', self._location)
        settings.setValue('dock_locations', self.saveState(VERSION_MAJOR))
        settings.setValue('sceneeditor_visibility', self._ui.action_SceneEditor.isChecked())
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        settings.setValue('state', self._snapshotDialog.serialise())
        settings.endGroup()

    def _readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        self.resize(settings.value('size', QtCore.QSize(1200, 900)))
        self.move(settings.value('pos', QtCore.QPoint(100, 150)))
        self._location = settings.value('location', QtCore.QDir.homePath())
        state = settings.value('dock_locations')
        if state is not None:
            self.restoreState(settings.value('dock_locations'), VERSION_MAJOR)
        self._ui.action_SceneEditor.setChecked(settings.value('sceneeditor_visibility', 'true') == 'true')
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        self._snapshotDialog.deserialise(settings.value('state', ''))
        settings.endGroup()

    def _setupViews(self, views):
        action_group = QtGui.QActionGroup(self)
        context = self._model.getContext()
        for v in views:
            v.setContext(context)
            self._ui.viewStackedWidget.addWidget(v)

            action_view = QtGui.QAction(v.name(), self)
            action_view.setCheckable(True)
            action_view.setChecked(True)
            action_view.setActionGroup(action_group)
            self._ui.menu_View.addAction(action_view)
            self._current_view = v

    def _viewReady(self):
        self._ui.widgetSceneEditor.setScene(self._current_view.getSceneviewer().getScene())

    def _dockWidgetTriggered(self):
        sender = self.sender()
        dock_widget = self._actionDockWidgetMap[sender]
        dock_widget.setVisible(sender.isChecked())

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

    def _dockWidgetVisibilityChanged(self, state):
        action = self._actionDockWidgetMap[self.sender()]
        action.setChecked(state)

    def _undoRedoStackIndexChanged(self, index):
        self._model.setCurrentUndoRedoIndex(index)

    def _aboutTriggered(self):
        d = AboutDialog(self)
        d.exec_()

    def _snapshotTriggered(self):
        self._snapshotDialog.setContext(self._model.getContext())
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

    def _openTriggered(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")

        if filename:
            self._location = os.path.dirname(filename)
            self._model.load(filename)
            region = self._model.getRootRegion()
            scene = region.getScene()
            self._ui.widgetSceneEditor.setScene(scene)
            self._current_view.getSceneviewer().setScene(scene)

    def confirmClose(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.isModified():
            ret = QtGui.QMessageBox.warning(self, 'Unsaved Changes', 'You have unsaved changes, would you like to save these changes now?',
                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                self._saveTriggered()

    def quitApplication(self):
        self.confirmClose()

        self._writeSettings()

        QtGui.qApp.quit()
