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

from opencmiss.neon.settings import mainsettings
from opencmiss.neon.core.neonregion import NeonRegion
from opencmiss.neon.core.neonspectrums import NeonSpectrums
from opencmiss.neon.core.neontessellations import NeonTessellations
from opencmiss.zinc.context import Context
from opencmiss.neon.core.neonlogger import NeonLogger
from opencmiss.neon.core.neonproject import NeonProject


class NeonDocument(object):

    def __init__(self):
        self._project = None
        self._zincContext = None
        self._rootRegion = None
        self._spectrums = None
        self._tessellations = None

    def initialiseVisualisationContents(self):
        self._zincContext = Context("Neon")

        # set up standard materials and glyphs
        materialmodule = self._zincContext.getMaterialmodule()
        materialmodule.defineStandardMaterials()
        glyphmodule = self._zincContext.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()

        zincRootRegion = self._zincContext.getDefaultRegion()
        self._rootRegion = NeonRegion(name=None, zincRegion=zincRootRegion, parent=None)
        self._rootRegion.connectRegionChange(self._regionChange)
        self._rootRegion._document = self

        self._spectrums = NeonSpectrums(self._zincContext)
        self._tessellations = NeonTessellations(self._zincContext)
        NeonLogger.setZincContext(self._zincContext)

    def freeVisualisationContents(self):
        """
        Deletes subobjects of document to help free memory held by Zinc objects earlier.
        """
        self._rootRegion.freeContents()
        del self._rootRegion
        del self._zincContext

    def initialiseProject(self):
        self._project = NeonProject()

    def freeProject(self):
        self._project = None

    def _regionChange(self, changedRegion, treeChange):
        """
        If root region has changed, set its new Zinc region as Zinc context's default region.
        :param changedRegion: The top region changed
        :param treeChange: True if structure of tree, or zinc objects reconstructed
        """
        if treeChange and (changedRegion is self._rootRegion):
            zincRootRegion = changedRegion.getZincRegion()
            self._zincContext.setDefaultRegion(zincRootRegion)

    def deserialize(self, state):
        '''
        :param dictInput: Python dict of Neon serialization
        :return: True on success, False on failure
        '''
        d = json.loads(state)
        if not (("OpenCMISS-Neon Version" in d) and ("RootRegion" in d)):
            NeonLogger.getLogger().error("Invalid format for Neon")
            return False
        neon_version = d["OpenCMISS-Neon Version"]
        # Not doing following here since issue 3924 prevents computed field wrappers being created, and graphics can't find fields
        # zincRegion.beginHierarchicalChange()
        result = True
        if "Project" in d:
            self._project.deserialize(d["Project"])
        if "Tessellations" in d:
            self._tessellations.deserialize(d["Tessellations"])
        if "Spectrums" in d:
            self._spectrums.deserialize(d["Spectrums"])
        self._rootRegion.deserialize(d["RootRegion"])
        if neon_version == '0.1.0':
            self._problem.setName('Generic')
        return result

    def serialize(self, basePath=None):
        outputVersion = [mainsettings.VERSION_MAJOR, mainsettings.VERSION_MINOR, mainsettings.VERSION_PATCH]
        dictOutput = {}
        dictOutput["OpenCMISS-Neon Version"] = outputVersion
        dictOutput["Project"] = self._project.serialize()
        dictOutput["Spectrums"] = self._spectrums.serialize()
        dictOutput["Tessellations"] = self._tessellations.serialize()
        dictOutput["RootRegion"] = self._rootRegion.serialize(basePath)
        return json.dumps(dictOutput, default=lambda o: o.__dict__, sort_keys=True, indent=2)

    def getZincContext(self):
        return self._zincContext

    def getRootRegion(self):
        return self._rootRegion

    def getSpectrums(self):
        return self._spectrums

    def getTessellations(self):
        return self._tessellations

    def setProject(self, project):
        self._project = project

    def getProject(self):
        return self._project
