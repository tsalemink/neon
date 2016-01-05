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
import importlib

from PySide import QtCore


def generateRelatedClasses(model, view):
    classes = []
    for row in range(model.rowCount()):
        index = model.index(row)
        name = model.data(index, QtCore.Qt.DisplayRole)
        module_name = importlib.import_module('.' + name.lower(), 'opencmiss.neon.ui.' + view)
        class_ = getattr(module_name, name)
        classes.append(class_())
#         view = class_(self._ui.stackedWidgetProblemView)
#         self._ui.stackedWidgetProblemView.addWidget(view)

    return classes
