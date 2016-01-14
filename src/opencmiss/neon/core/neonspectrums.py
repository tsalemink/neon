'''
   Copyright 2016 University of Auckland

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

from opencmiss.zinc.status import OK as ZINC_OK

class NeonSpectrums(object):
    """
    Manages and serialises Zinc Spectrums within Neon.
    Generates colour bar glyphs for spectrums, which is automatically done if if not found on loading.
    """

    def __init__(self, zincContext):
        self._zincContext = zincContext
        self._spectrummodule = zincContext.getSpectrummodule()

    def getZincContext(self):
        return self._zincContext

    def deserialize(self, dictInput):
        spectrumsDescription = json.dumps(dictInput)
        result = self._spectrummodule.readDescription(spectrumsDescription)
        if result != ZINC_OK:
            print("Failed to read spectrums")

    def serialize(self):
        spectrumsDescription = self._spectrummodule.writeDescription()
        dictOutput = json.loads(spectrumsDescription)
        return dictOutput
