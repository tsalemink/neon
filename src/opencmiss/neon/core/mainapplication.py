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
from opencmiss.neon.settings import mainsettings
from opencmiss.zinc.context import Context
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zinc.streamregion import StreaminformationRegion
from opencmiss.zinc.streamscene import StreaminformationScene


class MainApplication(object):

    def __init__(self):
        self._saveUndoRedoIndex = 0
        self._currentUntoRedoIndex = 0

        self._location = None
        self._recents = []

        self._context = Context("Main")

        # set up standard materials and glyphs
        materialmodule = self._context.getMaterialmodule()
        materialmodule.defineStandardMaterials()
        glyphmodule = self._context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()

        self._rootRegion = None
        self._document = None
        self._createBlankDocument()

    def _isDocumentValid(self, document):
        if ("OpenCMISS-Neon Version" in document) and ("RootRegion" in document):
            return True
        return False

    def _createBlankDocument(self):
        self._rootRegion = self._context.createRegion()
        self._document = {
            "OpenCMISS-Neon Version": [mainsettings.VERSION_MAJOR, mainsettings.VERSION_MINOR, mainsettings.VERSION_PATCH],
            "RootRegion": {}
        }

    def _updateZincDataInNeonRegion(self, neonRegion, zincRegion):
        scene = zincRegion.getScene()
        sceneDescription = scene.writeDescription()
        neonRegion["Scene"] = json.loads(sceneDescription)
        if not neonRegion["Scene"]:
            neonRegion.pop("Scene")  # remove empty scene description
        if "ChildRegions" in neonRegion:
            for neonChild in neonRegion["ChildRegions"]:
                childName = str(neonChild["Name"])
                zincChild = zincRegion.findChildByName(childName)
                self._updateZincDataInNeonRegion(neonChild, zincChild)

    def _updateZincDataInDocument(self):
        neonRegion = self._document["RootRegion"]
        zincRegion = self._rootRegion
        self._updateZincDataInNeonRegion(neonRegion, zincRegion)

    def _readModelSources(self, sources, zincRegion):
        streamInfo = zincRegion.createStreaminformationRegion()
        for source in sources:
            if source["Type"] == "File":
                fileName = str(source["FileName"])
                resource = streamInfo.createStreamresourceFile(fileName)
                if "Time" in source:
                    streamInfo.setResourceAttributeReal(resource, StreaminformationRegion.ATTRIBUTE_TIME, source["Time"])
                # if "Format" in source:
                #    format = source["Format"]
                #    if format == "EX":
                #        can't set per-resource file format
                #        streamInfo.setResourceFileFormat(resource, StreaminformationRegion.FILE_FORMAT_EX)
        result = zincRegion.read(streamInfo)
        if result != ZINC_OK:
            print("Failed to read model source")

    def _defineZincDataFromNeonRegion(self, neonRegion, zincRegion):
        if "Model" in neonRegion:
            model = neonRegion["Model"]
            if "Sources" in model:
                self._readModelSources(model["Sources"], zincRegion)
        if "Scene" in neonRegion:
            sceneDescription = json.dumps(neonRegion["Scene"])
            scene = zincRegion.getScene()
            scene.readDescription(sceneDescription, True)
        # for each neon region, ensure there is a matching zinc region in the same order, and recurse
        zincChildRef = zincRegion.getFirstChild()
        if "ChildRegions" in neonRegion:
            for neonChild in neonRegion["ChildRegions"]:
                childName = str(neonChild["Name"])
                zincChild = zincRegion.findChildByName(childName)
                if zincChildRef.isValid() and (zincChild == zincChildRef):
                    zincChildRef = zincChildRef.getNextSibling()
                else:
                    if not zincChild.isValid():
                        zincChild = zincRegion.createRegion()
                        zincChild.setName(childName)
                    zincRegion.insertChildBefore(zincChild, zincChildRef)
                self._defineZincDataFromNeonRegion(neonChild, zincChild)
        # ensure any new zinc regions (read from model sources) are added to neon region. No recursion needed
        if zincChildRef.isValid():
            if "ChildRegions" not in neonRegion:
                neonRegion["ChildRegions"] = []
            while zincChildRef.isValid():
                neonRegion["ChildRegions"].append({"Name": zincChildRef.getName()})
                zincChildRef = zincChildRef.getNextSibling()

    def _defineZincDataFromDocument(self, document):
        zincRegion = self._context.createRegion()
        # loop through document regions, load model data into Zinc
        neonRegion = document["RootRegion"]
        # Not doing here since issue 3924 prevents computed field wrappers being created, and graphics can't find fields
        # zincRegion.beginHierarchicalChange()
        try:
            self._defineZincDataFromNeonRegion(neonRegion, zincRegion)
        finally:
            # zincRegion.endChange() see zincRegion.beginHierarchicalChange()
            pass
        self._rootRegion = zincRegion

    def getContext(self):
        return self._context

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

    def save(self):
        self._updateZincDataInDocument()
        with open(self._location, 'w') as f:
            f.write(json.dumps(self._document, default=lambda o: o.__dict__, sort_keys=True, indent=2))

    def load(self, filename):
        self._location = filename
        with open(filename, 'r') as f:
            document = json.loads(f.read())
            if self._isDocumentValid(document):
                # set current directory to path from file, to support scripts and fieldml with external resources
                path = os.path.dirname(filename)
                os.chdir(path)
                self._defineZincDataFromDocument(document)
                self._document = document

    def getNeonRootRegion(self):
        return self._document["RootRegion"]

    def getZincRootRegion(self):
        return self._rootRegion

    def addRecent(self, recent):
        if recent in self._recents:
            index = self._recents.index(recent)
            del self._recents[index]

        self._recents.append(recent)

    def getRecents(self):
        return self._recents

    def clearRecents(self):
        self._recents = []
