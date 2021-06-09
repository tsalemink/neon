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
from PySide2 import QtCore


class ProjectModel(QtCore.QAbstractListModel):

    def __init__(self, parent=None):
        super(ProjectModel, self).__init__(parent)
        self._projects = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._projects)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return 'Project'
            else:
                return str(section)

        return ''

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            return self._projects[index.row()].getName()

        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        self._projects[index.row()] = value

    def insertRow(self, row, parent_index=None):
        self._projects.insert(row, None)
        return True

    def getDefaultProject(self):
        '''
        :return Project of the default 'Generic' type or None if not found
        '''
        for project in self._projects:
            if project.getIdentifier() == 'Generic':
                return project;
        return None

    def getProject(self, index):
        if not index.isValid():
            return None
        return self._projects[index.row()]

    def getProjectName(self, index):
        if not index.isValid():
            return ''

        return self._projects[index.row()].getName()

    def getProjectIdentifier(self, index):
        if not index.isValid():
            return None

        return self._projects[index.row()].getIdentifier()

    def getIndex(self, project):
        for r in range(self.rowCount()):
            index = self.index(r, 0)
            if project.getIdentifier() == self.getProjectIdentifier(index):
                return index

        index = self.index(-1, 0)
        return index
