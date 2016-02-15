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
import json
import os
from opencmiss.neon.core.neondocument import NeonDocument
from opencmiss.neon.core.problemmodel import ProblemModel
from opencmiss.neon.core.preferences import Preferences
from opencmiss.neon.core.neonproblems import names
from opencmiss.neon.core.misc.utils import importProblem
from opencmiss.neon.core.neonlogger import NeonLogger
import logging

class MainApplication(object):

    def __init__(self):
        self._saveUndoRedoIndex = 0
        self._currentUntoRedoIndex = 0

        self._location = None
        self._recents = []

        self._document = NeonDocument()

        self._problem_model = ProblemModel()
        self._setupModel()

        self._preferences = Preferences(self._problem_model)

    def _setupModel(self):
        for name in names:
            row = self._problem_model.rowCount()
            if self._problem_model.insertRow(row):
                index = self._problem_model.index(row)
                self._problem_model.setData(index, importProblem(name))

    def getZincContext(self):
        return self._document.getZincContext()

    def isModified(self):
        return self._saveUndoRedoIndex != self._currentUntoRedoIndex

    def setCurrentUndoRedoIndex(self, index):
        self._currentUntoRedoIndex = index

    def setSaveUndoRedoIndex(self, index):
        self._saveUndoRedoIndex = index

    def setLocation(self, location):
        self._location = location

    def getLocation(self):
        return self._location

    def new(self):
        # create a blank document
        self._document.freeContents()
        self._document = NeonDocument()

    def save(self):
        # make model sources relative to current location if possible
        # note that sources on different windows drives have absolute paths
        basePath = os.path.dirname(self._location)
        dictOutput = self._document.serialize(basePath)
        with open(self._location, 'w') as f:
            f.write(json.dumps(dictOutput, default=lambda o: o.__dict__, sort_keys=True, indent=2))

    def load(self, filename):
        self._location = filename
        with open(filename, 'r') as f:
            dictInput = json.loads(f.read())
            self._document.freeContents()
            self._document = NeonDocument()
            # set current directory to path from file, to support scripts and fieldml with external resources
            path = os.path.dirname(filename)
            os.chdir(path)
            if not self._document.deserialize(dictInput):
                NeonLogger.getLogger().error("Failed to load " + filename)
                # create a blank document
                self._document.freeContents()
                self._document = NeonDocument()

    def addRecent(self, recent):
        if recent in self._recents:
            index = self._recents.index(recent)
            del self._recents[index]
        self._recents.append(recent)

    def getRecents(self):
        return self._recents

    def clearRecents(self):
        self._recents = []

    def getDocument(self):
        return self._document

    def getProblemModel(self):
        return self._problem_model

    def getPreferences(self):
        return self._preferences
