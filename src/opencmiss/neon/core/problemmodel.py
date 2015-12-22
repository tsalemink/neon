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
from PySide import QtCore


class ProblemModel(QtCore.QAbstractListModel):

    def __init__(self, parent=None):
        super(ProblemModel, self).__init__(parent)
        self._problems = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._problems)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return 'Problem'
            else:
                return str(section)

        return ''

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            return self._problems[index.row()].getName()

        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        self._problems[index.row()] = value

    def insertRow(self, row, parent_index=None):
        self._problems.insert(row, None)
        return True
