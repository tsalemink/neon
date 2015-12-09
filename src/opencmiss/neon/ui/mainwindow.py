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

        # List of possible views
        view_list = [DefaultView(self)]
        self._shared_gl_widget = view_list[0].getShareGLWidget()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self, self._shared_gl_widget)

        self._ui.menu_View.addAction(self._ui.dockWidgetSceneEditor.toggleViewAction())
        self._ui.menu_View.addAction(self._ui.dockWidgetSpectrumEditor.toggleViewAction())
        self._ui.menu_View.addAction(self._ui.dockWidgetTessellationEditor.toggleViewAction())
        self._ui.menu_View.addAction(self._ui.dockWidgetTimeEditor.toggleViewAction())
        self._ui.menu_View.addSeparator()

        self._location = None  # The last location/directory used by the application
        self._current_view = None
        self._recents = []

        self._undoRedoStack = QtGui.QUndoStack(self)

        self._shareContext()

        # Pre-create dialogs
        self._createDialogs()

        self._readSettings()

        self._setupViews(view_list)

        self._makeConnections()

        # Set the undo redo stack state
        self._undoRedoStack.push(CommandEmpty())
        self._undoRedoStack.clear()

        self._updateUi()

    def _makeConnections(self):
        self._ui.action_Quit.triggered.connect(self.quitApplication)
        self._ui.action_New.triggered.connect(self._newTriggered)
        self._ui.action_Open.triggered.connect(self._openTriggered)
        self._ui.action_About.triggered.connect(self._aboutTriggered)
        self._ui.action_Save.triggered.connect(self._saveTriggered)
        self._ui.action_Save_As.triggered.connect(self._saveAsTriggered)
        self._ui.action_Snapshot.triggered.connect(self._snapshotTriggered)

        self._undoRedoStack.indexChanged.connect(self._undoRedoStackIndexChanged)
        self._undoRedoStack.canUndoChanged.connect(self._ui.action_Undo.setEnabled)
        self._undoRedoStack.canRedoChanged.connect(self._ui.action_Redo.setEnabled)

        self._current_view.graphicsInitialized.connect(self._viewReady)

    def _updateUi(self):
        modified = self._model.isModified()
        self._ui.action_Save.setEnabled(modified)
        self._ui.action_Clear.setEnabled(len(self._recents))

    def _createDialogs(self):
        self._snapshotDialog = SnapshotDialog(self, self._shared_gl_widget)
        self._snapshotDialog.setContext(self._model.getContext())

    def _writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.setValue('location', self._location)
        settings.setValue('dock_locations', self.saveState(VERSION_MAJOR))
        settings.setValue('sceneeditor_visibility', self._ui.action_SceneEditor.isChecked())
        settings.setValue('spectrumeditor_visibility', self._ui.action_SpectrumEditor.isChecked())
        settings.beginWriteArray('recents')
        for i, r in enumerate(self._recents):
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
        self.resize(settings.value('size', QtCore.QSize(1200, 900)))
        self.move(settings.value('pos', QtCore.QPoint(100, 150)))
        self._location = settings.value('location', QtCore.QDir.homePath())
        state = settings.value('dock_locations')
        if state is not None:
            self.restoreState(settings.value('dock_locations'), VERSION_MAJOR)
        self._ui.action_SceneEditor.setChecked(settings.value('sceneeditor_visibility', 'true') == 'true')
        self._ui.action_SpectrumEditor.setChecked(settings.value('spectrumeditor_visibility', 'true') == 'true')
        size = settings.beginReadArray('recents')
        for i in range(size):
            settings.setArrayIndex(i)
            self._recents.append(settings.value('item'))
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        self._snapshotDialog.deserialise(settings.value('state', ''))
        settings.endGroup()

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

    def _viewReady(self):
        self._ui.dockWidgetContentsSceneEditor.setScene(self._current_view.getSceneviewer().getScene())

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
        print('Implement me!')

    def _openTriggered(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")

        if filename:
            self._location = os.path.dirname(filename)
            self._model.load(filename)
            region = self._model.getRootRegion()
            scene = region.getScene()
            self._ui.dockWidgetContentsSceneEditor.setScene(scene)
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
