'''
   Copyright 2016 University of Auckland

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
"""
Zinc Field List Editor Widget

Allows a Zinc Field object to be created/edited in Qt / Python.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from PySide import QtCore, QtGui

from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zinc.field import Field

from opencmiss.neon.ui.editors.ui_fieldlisteditorwidget import Ui_FieldListEditorWidget


class FieldListEditorWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        '''
        Call the super class init functions
        '''
        QtGui.QWidget.__init__(self, parent)
        self._fieldmodule = None
        # Using composition to include the visual element of the GUI.
        self.ui = Ui_FieldListEditorWidget()
        self._fieldItems = None
        self._neonRegion = None
        self._timekeeper = None
        self.ui.setupUi(self)
        self._makeConnections()
        self._field = None
        
    @QtCore.Slot(Field, str)
    def editorCreateField(self, field, fieldType):
        self._neonRegion.addFieldTypeToDict(field, fieldType)
        self.setField(field)
        
    def _makeConnections(self):
        self.ui.field_listview.clicked.connect(self.fieldListItemClicked)
        self.ui.addFieldButton.clicked.connect(self.addFieldClicked)
        self.ui.field_editor._fieldCreated.connect(self.editorCreateField)

    def getFieldmodule(self):
        '''
        Get the fieldmodule currently in the editor
        '''
        return self._fieldmodule
    
    def _fieldmoduleCallback(self, fieldmoduleevent):
        '''
        Callback for change in fields; may need to rebuild field list
        '''
        changeSummary = fieldmoduleevent.getSummaryFieldChangeFlags()
        # print "_fieldmoduleCallback changeSummary =", changeSummary
        if (0 != (changeSummary & (Field.CHANGE_FLAG_IDENTIFIER | Field.CHANGE_FLAG_ADD | Field.CHANGE_FLAG_REMOVE))):
            self._buildFieldsList()

    def setTimekeeper(self, timekeeper):
        '''
        Set the current scene in the editor
        '''
        if not (timekeeper and timekeeper.isValid()):
            self._timekeeper = None
        else:
            self._timekeeper = timekeeper
        if self._timekeeper:
            self.ui.field_editor.setTimekeeper(self._timekeeper)

    def setFieldmodule(self, fieldmodule):
        '''
        Set the current scene in the editor
        '''
        if not (fieldmodule and fieldmodule.isValid()):
            self._fieldmodule = None
        else:
            self._fieldmodule = fieldmodule
        if self._fieldmodule:
            self.ui.field_editor.setFieldmodule(self._fieldmodule)
        self._buildFieldsList()
        if self._fieldmodule:
            self._fieldmodulenotifier = self._fieldmodule.createFieldmodulenotifier()
            self._fieldmodulenotifier.setCallback(self._fieldmoduleCallback)
        else:
            self._fieldmodulenotifier = None
        
    def setNeonRegion(self, neonRegion):
        '''
        Set the current scene in the editor
        '''
        self._neonRegion = neonRegion
        
    def listItemEdited(self, item):
        field = item.data()
        if field and field.isValid():
            newName = item.text()
            oldName = field.getName()
            if newName != oldName:
                if field.setName(newName) != ZINC_OK:
                    item.setText(field.getName())
                self._neonRegion.replaceFieldTypeKey(oldName, newName)
        
    def _buildFieldsList(self):
        '''
        Fill the graphics list view with the list of graphics for current region/scene
        '''
        if self._fieldItems is not None:
            self._fieldItems.clear()  # Must clear or holds on to field references
        self._fieldItems = QtGui.QStandardItemModel(self.ui.field_listview)
        selectedIndex = None
        if self._fieldmodule:
            selectedField = self.ui.field_editor.getField()
            fieldIterator = self._fieldmodule.createFielditerator()
            field = fieldIterator.next()
            while field and field.isValid():
                name = field.getName()
                item = QtGui.QStandardItem(name)
                item.setData(field)
                item.setCheckable(False)
                item.setEditable(True)
                self._fieldItems.appendRow(item)
                if selectedField and field == selectedField:
                    selectedIndex = self._fieldItems.indexFromItem(item)
                field = fieldIterator.next()
        self.ui.field_listview.setModel(self._fieldItems)
        self._fieldItems.itemChanged.connect(self.listItemEdited)
        # self.ui.graphics_listview.setMovement(QtGui.QListView.Snap)
        # self.ui.graphics_listview.setDragDropMode(QtGui.QListView.InternalMove)
        # self.ui.graphics_listview.setDragDropOverwriteMode(False)
        # self.ui.graphics_listview.setDropIndicatorShown(True)
        if selectedIndex:
            self.ui.field_listview.setCurrentIndex(selectedIndex)
        self.ui.field_listview.show()
        
    def _displayField(self):
        if self._field and self._field.isValid():
            selectedIndex = None
            i = 0
            # loop through the items until you get None, which
            # means you've passed the end of the list
            while self._fieldItems.item(i):
                field = self._fieldItems.item(i).data()
                if self._field == field:
                    selectedIndex = self._fieldItems.indexFromItem(self._fieldItems.item(i))
                    break
                i += 1
            if selectedIndex:
                self.ui.field_listview.setCurrentIndex(selectedIndex)
            name = self._field.getName()
            fieldType = None
            fieldTypeDict = self._neonRegion.getFieldTypeDict()
            if name in fieldTypeDict:
                fieldType = fieldTypeDict[name]
                self.ui.field_editor.setField(self._field, fieldType)
            else:
                self.ui.field_editor.setField(self._field, None)
        else:
            self.field_listview.clearSelection()
            self.ui.field_editor.setField(None, None)

    def fieldListItemClicked(self, modelIndex):
        model = modelIndex.model()
        item = model.item(modelIndex.row())
        field = item.data()
        self._field = field
        self._displayField()
            
    def setField(self, field):
        '''
        Set the current selected field
        '''
        if not field or not field.isValid():
            self._field = None
        else:
            self._field = field
        self._displayField()
            
    def addFieldClicked(self):
        '''do the add field stuff'''
        self.ui.field_editor.enterCreateMode()

