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

from opencmiss.neon.core.neonmodelsources import deserializeNeonModelSource
from opencmiss.zinc.status import OK as ZINC_OK


class NeonRegion(object):

    def __init__(self, name, zincRegion, parent=None):
        self._name = name
        self._parent = parent
        self._children = []
        self._modelSources = []
        self._zincRegion = zincRegion

    def _loadModelSources(self):
        streamInfo = self._zincRegion.createStreaminformationRegion()
        for modelSource in self._modelSources:
            modelSource.addToZincStreaminformationRegion(streamInfo)
        result = self._zincRegion.read(streamInfo)
        if result != ZINC_OK:
            print("Failed to read model source")

    def deserialize(self, dictInput):
        if "Model" in dictInput:
            model = dictInput["Model"]
            if "Sources" in model:
                for dictModelSource in model["Sources"]:
                    modelSource = deserializeNeonModelSource(dictModelSource)
                    if modelSource:
                        self._modelSources.append(modelSource)
                self._loadModelSources()
        if "Scene" in dictInput:
            scene = self._zincRegion.getScene()
            sceneDescription = json.dumps(dictInput["Scene"])
            result = scene.readDescription(sceneDescription, True)
            if result != ZINC_OK:
                print("Failed to read scene")
        # following assumes no neon child regions exist, i.e. we are deserializing into a blank region
        # for each neon region, ensure there is a matching zinc region in the same order, and recurse
        zincChildRef = self._zincRegion.getFirstChild()
        if "ChildRegions" in dictInput:
            for dictChild in dictInput["ChildRegions"]:
                childName = str(dictChild["Name"])
                # see if zinc child with this name created by model source here or in ancestor region
                zincChild = self._zincRegion.findChildByName(childName)
                if zincChildRef.isValid() and (zincChild == zincChildRef):
                    zincChildRef = zincChildRef.getNextSibling()
                else:
                    if not zincChild.isValid():
                        zincChild = self._zincRegion.createRegion()
                        zincChild.setName(childName)
                    self._zincRegion.insertChildBefore(zincChild, zincChildRef)
                neonChild = NeonRegion(childName, zincChild, self)
                self._children.append(neonChild)
                neonChild.deserialize(dictChild)
        # ensure any new zinc regions (read from model sources) are added to neon region. No recursion needed
        if zincChildRef.isValid():
            while zincChildRef.isValid():
                childName = zincChildRef.getName()
                neonChild = NeonRegion(childName, zincChildRef, self)
                self._children.append(neonChild)
                zincChildRef = zincChildRef.getNextSibling()

    def serialize(self):
        dictOutput = {}
        if self._name:
            dictOutput["Name"] = self._name
        dictOutput["Model"] = {}
        if self._modelSources:
            tmpOutput = []
            for modelSource in self._modelSources:
                tmpOutput.append(modelSource.serialize())
            dictOutput["Model"]["Sources"] = tmpOutput
        if not dictOutput["Model"]:
            dictOutput.pop("Model")
        if self._zincRegion:
            scene = self._zincRegion.getScene()
            sceneDescription = scene.writeDescription()
            dictOutput["Scene"] = json.loads(sceneDescription)
        if self._children:
            tmpOutput = []
            for child in self._children:
                tmpOutput.append(child.serialize())
            dictOutput["ChildRegions"] = tmpOutput
        return dictOutput

    def getName(self):
        return self._name

    def getPath(self):
        if self._name:
            return self._parent.getPath() + self._name + "/"
        return "/"

    def getParent(self):
        return self._parent

    def getZincRegion(self):
        return self._zincRegion

    def getChildCount(self):
        return len(self._children)

    def getChild(self, index):
        return self._children[index]
