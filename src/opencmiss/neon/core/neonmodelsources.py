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
from opencmiss.zinc.streamregion import StreaminformationRegion


class NeonModelSourceFile(object):

    def __init__(self, fileName=None, dictInput=None):
        self._time = None
        self._format = None
        if fileName:
            self._fileName = fileName
        else:
            self._deserialize(dictInput)

    def addToZincStreaminformationRegion(self, streamInfo):
        resource = streamInfo.createStreamresourceFile(self._fileName)
        if self._time is not None:
            streamInfo.setResourceAttributeReal(resource, StreaminformationRegion.ATTRIBUTE_TIME, self._time)
        # if self._format is not None:
        #    if format == "EX":
        #        #can't set per-resource file format
        #        #streamInfo.setResourceFileFormat(resource, StreaminformationRegion.FILE_FORMAT_EX)

    def setTime(self, time):
        self._time = time

    def _deserialize(self, dictInput):
        self._fileName = str(dictInput["FileName"])
        if "Time" in dictInput:
            self._time = dictInput["Time"]
        if "Format" in dictInput:
            self._format = dictInput["Format"]

    def serialize(self):
        dictOutput = {}
        dictOutput["Type"] = "FILE"
        dictOutput["FileName"] = self._fileName
        if self._time is not None:
            dictOutput["Time"] = self._time
        return dictOutput


def deserializeNeonModelSource(dictInput):
    '''
    Factory method for creating the appropriate neon model source type from the dict serialization
    '''
    if "Type" not in dictInput:
        print("Model source is missing Type")
        return None
    modelSource = None
    typeString = dictInput["Type"].upper()  # wasn't originally uppercase
    if typeString == "FILE":
        modelSource = NeonModelSourceFile(dictInput=dictInput)
    else:
        print("Model source has unrecognised Type \"" + typeString + "\"")
    return modelSource
