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
from opencmiss.zinc.context import Context

class MainApplication(object):
    
    
    def __init__(self):
        self._saveUndoRedoIndex = 0
        self._currentUntoRedoIndex = 0
        
        self._context = Context("Main")
    
    def getContext(self):
        return self._context
    
    def isModified(self):
        return self._saveUndoRedoIndex != self._currentUntoRedoIndex
    
    def setCurrentUndoRedoIndex(self, index):
        self._currentUntoRedoIndex = index
        
    def setSaveUndoRedoIndex(self, index):
        self._saveUndoRedoIndex = index
        
    def load(self, filename):
        pass
    
    
    