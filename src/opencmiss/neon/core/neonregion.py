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
from opencmiss.neon.core.neonmodelsources import NeonModelSourceFile, deserializeNeonModelSource
from opencmiss.zinc.status import OK as ZINC_OK

class NeonRegion(object):

    def __init__(self, name, zincRegion, parent=None):
        self._name = name
        self._parent = parent
        self._children = []
        self._modelSources = []
        self._zincRegion = zincRegion
        # record whether region was created by ancestor model source; see: _reloadModelSources
        self._ancestorModelSourceCreated = False
        # callback class, only for root region
        if not parent:
            self._regionChangeCallbacks = []

    def _assign(self, source):
        """
        Replace contents of self with that of source
        """
        self._name = source._name
        self._parent = source._parent
        self._children = source._children
        self._modelSources = source._modelSources
        self._zincRegion = source._zincRegion
        self._ancestorModelSourceCreated = source._ancestorModelSourceCreated

    def _informRegionChange(self, treeChange):
        """
        Called by regions when their tree structure changes or zinc regions are rebuilt.
        Informs registered clients of change. Root region handle these signals for whole tree.
        """
        rootRegion = self
        while rootRegion._parent:
            rootRegion = rootRegion._parent
        for callback in rootRegion._regionChangeCallbacks:
            callback(self, treeChange)

    def _getDescendantCount(self):
        descendantCount = len(self._children)
        for child in self._children:
            descendantCount += child._getDescendantCount()
        return descendantCount

    def connectRegionChange(self, callableObject):
        """
        Request callbacks on region tree changes.
        :param callableObject: Callable object taking a NeonRegion argument and a boolean flag which is True if tree
        structure below region needs to be rebuilt.
        """
        self._regionChangeCallbacks.append(callableObject)

    def _loadModelSourceStreams(self, streamInfo):
        self._zincRegion.beginHierarchicalChange()
        result = self._zincRegion.read(streamInfo)
        fieldmodule = self._zincRegion.getFieldmodule()
        fieldmodule.defineAllFaces()
        self._zincRegion.endHierarchicalChange()
        return result

    def _loadModelSource(self, modelSource):
        descendantCountBefore = self._getDescendantCount()
        streamInfo = self._zincRegion.createStreaminformationRegion()
        modelSource.addToZincStreaminformationRegion(streamInfo)
        result = self._loadModelSourceStreams(streamInfo)
        if result != ZINC_OK:
            print("Failed to read model source")
        else:
            # discover new child regions read from model sources:
            self.deserialize({})
            descendantCountAfter = self._getDescendantCount()
            self._informRegionChange(descendantCountAfter > descendantCountBefore)

    def _loadModelSources(self):
        streamInfo = self._zincRegion.createStreaminformationRegion()
        for modelSource in self._modelSources:
            modelSource.addToZincStreaminformationRegion(streamInfo)
        result = self._loadModelSourceStreams(streamInfo)
        if result != ZINC_OK:
            print("Failed to read model sources")

    def _reload(self):
        """
        Must be called when already-loaded model source modified or deleted.
        Saves and reloads region tree, starting at ancestor if this region was created by its model source.
        :return: Neon Region to rebuild tree from, can be ancestor of self
        """
        if self._ancestorModelSourceCreated:
            self._parent._reload()
        else:
            # beware this breaks parent/child links such as current selection / hierarchical groups
            dictSave = self.serialize()
            zincRegion = self._zincRegion.createRegion()
            if self._name:
                zincRegion.setName(self._name)
            tmpRegion = NeonRegion(self._name, zincRegion, self._parent)
            tmpRegion.deserialize(dictSave)
            if self._parent is not None:
                # replace old zinc child region with new one in zinc parent
                zincSiblingAfter = self._zincRegion.getNextSibling()
                self._parent._zincRegion.removeChild(self._zincRegion)
                self._parent._zincRegion.insertChildBefore(zincRegion, zincSiblingAfter)
            self._assign(tmpRegion)
            self._informRegionChange(True)

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
                ancestorModelSourceCreated = True
                zincChild = self._zincRegion.findChildByName(childName)
                if zincChildRef.isValid() and (zincChild == zincChildRef):
                    zincChildRef = zincChildRef.getNextSibling()
                else:
                    if not zincChild.isValid():
                        zincChild = self._zincRegion.createRegion()
                        zincChild.setName(childName)
                        ancestorModelSourceCreated = False
                    self._zincRegion.insertChildBefore(zincChild, zincChildRef)
                neonChild = NeonRegion(childName, zincChild, self)
                neonChild._ancestorModelSourceCreated = ancestorModelSourceCreated
                self._children.append(neonChild)
                neonChild.deserialize(dictChild)
        # ensure any new zinc regions (read from model sources) are added to neon region, recurse to find subregions
        while zincChildRef.isValid():
            childName = zincChildRef.getName()
            neonChild = NeonRegion(childName, zincChildRef, self)
            neonChild._ancestorModelSourceCreated = True
            self._children.append(neonChild)
            neonChild.deserialize({})
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

    def getDisplayName(self):
        if self._name:
            return self._name
        elif not self._parent:
            return "/"
        return "?"

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

    def getModelSources(self):
        return self._modelSources

    def addModelSource(self, modelSource):
        """
        Add model source, applying it if not currently editing
        :param modelSource: The model source to add
        """
        self._modelSources.append(modelSource)
        if not modelSource.isEdit():
            self.applyModelSource(modelSource)

    def applyModelSource(self, modelSource):
        """
        Apply model source, loading it or reloading it with all other sources as required
        :param modelSource: The model source to apply
        """
        modelSource.setEdit(False)
        if modelSource.isLoaded():
            self._reload()
        else:
            self._loadModelSource(modelSource)

    def removeModelSource(self, modelSource):
        """
        Remove model source, reloading model if it removed source had been loaded
        :param modelSource: The model source to remove
        """
        self._modelSources.remove(modelSource)
        if modelSource.isLoaded():
            self._reload()
