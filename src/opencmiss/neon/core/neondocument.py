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
from opencmiss.neon.settings import mainsettings
from opencmiss.neon.core.neonregion import NeonRegion
from opencmiss.zinc.context import Context


class NeonDocument(object):

    def __init__(self):
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

    def freeContents(self):
        """
        Deletes subobjects of document to help free memory held by Zinc objects earlier.
        """
        self._rootRegion.freeContents()
        del self._rootRegion
        del self._zincContext

    def _regionChange(self, changedRegion, treeChange):
        """
        If root region has changed, set its new Zinc region as Zinc context's default region.
        :param changedRegion: The top region changed
        :param treeChange: True if structure of tree, or zinc objects reconstructed
        """
        if treeChange and (changedRegion is self._rootRegion):
            zincRootRegion = changedRegion.getZincRegion()
            self._zincContext.setDefaultRegion(zincRootRegion)

    def deserialize(self, dictInput):
        '''
        :param dictInput: Python dict of Neon serialization
        :return: True on success, False on failure
        '''
        if not (("OpenCMISS-Neon Version" in dictInput) and ("RootRegion" in dictInput)):
            print("Invalid format for Neon")
            return False
        _ = dictInput["OpenCMISS-Neon Version"]
        # Not doing following here since issue 3924 prevents computed field wrappers being created, and graphics can't find fields
        # zincRegion.beginHierarchicalChange()
        result = True
        try:
            self._rootRegion.deserialize(dictInput["RootRegion"])
        except:
            print("Exception in NeonDocument.deserialize")
            result = False
        finally:
            # zincRegion.endChange() see zincRegion.beginHierarchicalChange()
            pass
        return result

    def serialize(self):
        outputVersion = [mainsettings.VERSION_MAJOR, mainsettings.VERSION_MINOR, mainsettings.VERSION_PATCH]
        dictOutput = {}
        dictOutput["OpenCMISS-Neon Version"] = outputVersion
        dictOutput["RootRegion"] = self._rootRegion.serialize()
        return dictOutput

    def getZincContext(self):
        return self._zincContext

    def getRootRegion(self):
        return self._rootRegion
