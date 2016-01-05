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


class NeonDocument(object):

    def __init__(self, zincContext):
        self._zincContext = zincContext
        zincRootRegion = zincContext.createRegion()
        self._rootRegion = NeonRegion(name=None, zincRegion=zincRootRegion, parent=None)
        self._rootRegion._document = self

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

    def getRootRegion(self):
        return self._rootRegion
