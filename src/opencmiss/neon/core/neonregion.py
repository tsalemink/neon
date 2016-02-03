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
from opencmiss.neon.core.neonlogger import NeonLogger

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

    #def __del__(self):
    #    print("NeonRegion.__del__ " + self.getDisplayName())

    def freeContents(self):
        """
        Deletes subobjects of region to help free memory held by Zinc objects earlier.
        """
        del self._zincRegion
        for child in self._children:
            child.freeContents()

    def _createBlankCopy(self):
        zincRegion = self._zincRegion.createRegion()
        if self._name:
            zincRegion.setName(self._name)
        blankRegion = NeonRegion(self._name, zincRegion, self._parent)
        return blankRegion

    def _assign(self, source):
        """
        Replace contents of self with that of source. Fixes up Zinc parent/child region relationships.
        """
        if self._parent:
            oldZincRegion = self._zincRegion
            zincSiblingAfter = oldZincRegion.getNextSibling()
        else:
            oldZincRegion = None
            zincSiblingAfter = None
        self.freeContents()
        self._name = source._name
        # self._parent = source._parent should not be changed
        self._children = source._children
        for child in self._children:
            child._parent = self
        self._modelSources = source._modelSources
        self._zincRegion = source._zincRegion
        # self._ancestorModelSourceCreated is unchanged
        if self._parent:
            self._parent._zincRegion.removeChild(oldZincRegion)
            self._parent._zincRegion.insertChildBefore(self._zincRegion, zincSiblingAfter)

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
        streamInfo = self._zincRegion.createStreaminformationRegion()
        modelSource.addToZincStreaminformationRegion(streamInfo)
        result = self._loadModelSourceStreams(streamInfo)
        if result != ZINC_OK:
            NeonLogger.getLogger().error("Failed to read model source")
        else:
            newRegionCount = self._discoverNewZincRegions()
            self._informRegionChange(newRegionCount > 0)

    def _loadModelSources(self):
        streamInfo = self._zincRegion.createStreaminformationRegion()
        for modelSource in self._modelSources:
            modelSource.addToZincStreaminformationRegion(streamInfo)
        result = self._loadModelSourceStreams(streamInfo)
        if result != ZINC_OK:
             NeonLogger.getLogger().error("Failed to read model sources")

    def _reload(self):
        """
        Must be called when already-loaded model source modified or deleted.
        Saves and reloads region tree, starting at ancestor if this region was created by its model source.
        """
        if self._ancestorModelSourceCreated:
            self._parent._reload()
        else:
            # beware this breaks parent/child links such as current selection / hierarchical groups
            dictSave = self.serialize()
            tmpRegion = self._createBlankCopy()
            tmpRegion.deserialize(dictSave)
            self._assign(tmpRegion)
            self._informRegionChange(True)

    def _discoverNewZincRegions(self):
        """
        Ensure there are Neon regions for every Zinc Region in tree
        :return: Number of new descendant regions created
        """
        newRegionCount = 0
        zincChildRef = self._zincRegion.getFirstChild()
        while zincChildRef.isValid():
            childName = zincChildRef.getName()
            neonChild = self._findChildByName(childName)
            if not neonChild:
                neonChild = NeonRegion(childName, zincChildRef, self)
                neonChild._ancestorModelSourceCreated = True
                self._children.append(neonChild)
                newRegionCount += (1 + neonChild._discoverNewZincRegions())
            zincChildRef = zincChildRef.getNextSibling()
        return newRegionCount

    def _findChildByName(self, name):
        for child in self._children:
            if child._name == name:
                return child
        return None

    def _generateChildName(self):
        count = len(self._children) + 1
        while True:
            name = "region" + str(count)
            if not self._findChildByName(name):
                return name
            count += 1
        return None

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
                 NeonLogger.getLogger().error("Failed to read scene")
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
        self._discoverNewZincRegions()

    def serialize(self, basePath=None):
        dictOutput = {}
        if self._name:
            dictOutput["Name"] = self._name
        dictOutput["Model"] = {}
        if self._modelSources:
            tmpOutput = []
            for modelSource in self._modelSources:
                tmpOutput.append(modelSource.serialize(basePath))
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
                tmpOutput.append(child.serialize(basePath))
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

    def clear(self):
        """
        Clear all contents of region. Can be called for root region
        """
        tmpRegion = self._createBlankCopy()
        self._assign(tmpRegion)
        if self._ancestorModelSourceCreated:
            self._reload()
        else:
            self._informRegionChange(True)

    def createChild(self):
        """
        Create a child region with a default name
        :return: The new Neon Region
        """
        childName = self._generateChildName()
        zincRegion = self._zincRegion.createChild(childName)
        if zincRegion.isValid():
            childRegion = NeonRegion(childName, zincRegion, self)
            self._children.append(childRegion)
            self._informRegionChange(True)
            return childRegion
        return None

    def removeChild(self, childRegion):
        """
        Remove child region and destroy
        """
        self._children.remove(childRegion)
        self._zincRegion.removeChild(childRegion._zincRegion)
        childRegion._parent = None
        childRegion.freeContents()
        if childRegion._ancestorModelSourceCreated:
            self._reload()
        else:
            self._informRegionChange(True)

    def remove(self):
        """
        Remove self from region tree and destroy; replace with blank region if root
        """
        if self._parent:
            self._parent.removeChild(self)
        else:
            self.clear()

    def setName(self, name):
        if not self._parent:
            return False
        if len(name) == 0:
            return False
        if self._ancestorModelSourceCreated:
            return False
        if ZINC_OK != self._zincRegion.setName(name):
            return False
        self._name = name
        self._informRegionChange(True)
        return True

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
