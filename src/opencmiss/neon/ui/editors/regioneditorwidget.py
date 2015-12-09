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
"""
OpenCMISS-Neon Region Editor Widget

Displays and allows editing of the the Neon region tree.
"""

from PySide import QtCore, QtGui

from opencmiss.neon.ui.editors.ui_regioneditorwidget import Ui_RegionEditorWidget

class RegionTreeItem(object):

    def __init__(self, neonRegion, row, parent=None):
        self._neonRegion = neonRegion
        self._row = row
        self._parent = parent
        self._children = []
        if "ChildRegions" in neonRegion:
            childRow = 0
            for neonChild in neonRegion["ChildRegions"]:
                self._children.append(RegionTreeItem(neonChild, childRow, self))
                childRow += 1

    def neonRegion(self):
        return self._neonRegion

    def row(self):
        return self._row

    def parent(self):
        return self._parent

    def child(self, i):
        if i < len(self._children):
            return self._children[i]
        return None

    def childCount(self):
        return len(self._children)

    def setRootChild(self, neonRootItem):
        self._children = [ neonRootItem ]

class RegionTreeModel(QtCore.QAbstractItemModel):

    def __init__(self, neonRootRegion, parent):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self._neonRootRegion = neonRootRegion
        self._rootItem = RegionTreeItem({}, 0)
        if neonRootRegion is not None:
            neonRootItem = RegionTreeItem(neonRootRegion, 0, self._rootItem)
            self._rootItem.setRootChild(neonRootItem)

    def setRootRegion(self, neonRootRegion):
        neonRootItem = RegionTreeItem(neonRootRegion, 0)
        self._rootItem.setRootChild(neonRootItem)

    def columnCount(self, parentIndex):
        return 1

    def flags(self, index):
        if not index.isValid():
            return 0
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    #def headerData(self, section, orientation, role):
    #    if (orientation == QtCore.Qt.Horizontal) and (role == QtCore.Qt.DisplayRole) and (section == 0):
    #         return 'Name'
    #    return None

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QtCore.QModelIndex()
        if parentIndex.isValid():
            parentItem = parentIndex.internalPointer()
        else:
            parentItem = self._rootItem
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QtCore.QModelIndex()

    def rowCount(self, parentIndex):
        if parentIndex.column() > 0:
            return 0
        if parentIndex.isValid():
            parentItem = parentIndex.internalPointer()
        else:
            parentItem = self._rootItem
        return parentItem.childCount()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        item = index.internalPointer()
        parentItem = item.parent()
        if parentItem and (parentItem is not self._rootItem):
            return self.createIndex(parentItem.row(), 0, parentItem)
        return QtCore.QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None
        item = index.internalPointer()
        if (role == QtCore.Qt.DisplayRole) and (index.column() == 0):
            neonRegion = item.neonRegion()
            if "Name" in neonRegion:
                return neonRegion["Name"]
            else:
                return "/"
        return None

    def getPathToIndex(self, index):
        if not index.isValid():
            return ""
        item = index.internalPointer()
        neonRegion = item.neonRegion()
        if "Name" in neonRegion:
            return self.getPathToIndex(self.parent(index)) + str(neonRegion["Name"]) + "/"
        return "/"

class RegionEditorWidget(QtGui.QWidget):

    regionSelected = QtCore.Signal(object)

    def __init__(self, parent=None):
        '''
        Call the super class init functions
        '''
        QtGui.QWidget.__init__(self, parent)
        self._neonRootRegion = None
        self._zincRootRegion = None
        self._regionItems = None
        # Using composition to include the visual element of the GUI.
        self._ui = Ui_RegionEditorWidget()
        self._ui.setupUi(self)
        self._makeConnections()

    def _makeConnections(self):
        self._ui.treeViewRegion.clicked.connect(self._regionTreeItemClicked)

    def setRootRegion(self, neonRootRegion, zincRootRegion):
        self._neonRootRegion = neonRootRegion
        self._zincRootRegion = zincRootRegion
        # rebuild tree
        self._buildTree()

    def _buildTree(self):
        self._regionItems = RegionTreeModel(self._neonRootRegion, None)
        self._ui.treeViewRegion.setModel(self._regionItems)
        self._ui.treeViewRegion.header().hide()
        self._ui.treeViewRegion.expandAll()
        #if selectedIndex:
        #    self._ui.treeViewRegion.setCurrentIndex(selectedIndex)
        self._ui.treeViewRegion.show()

    def _regionTreeItemClicked(self, index):
        '''
        Either changes visibility flag or selects current graphics
        '''
        model = index.model()
        regionPath = model.getPathToIndex(index)
        print("Clicked on region " + regionPath)
        zincRegion = self._zincRootRegion.findSubregionAtPath(regionPath)
        self.regionSelected.emit(zincRegion)
