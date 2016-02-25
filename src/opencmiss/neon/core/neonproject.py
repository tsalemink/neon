"""
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
"""
import json


class NeonProject(object):
    """
    Manages and serialises Zinc Spectrums within Neon.
    Generates colour bar glyphs for spectrums, which is automatically done if if not found on loading.
    """

    def __init__(self):
#         self._name = None
        self._problem = None
        self._simulation = None

    def getName(self):
        return self._problem.getName()

    def getIdentifier(self):
        return self._problem.getIdentifier()

    def setProblem(self, problem):
        self._problem = problem

    def getProblem(self):
        return self._problem

    def setSimulation(self, simulation):
        self._simulation = simulation

    def getSimulation(self):
        return self._simulation

    def deserialize(self, dictInput):
        description = json.dumps(dictInput)
        self._name = description['name'] if 'name' in description else None

    def serialize(self):
        description = {'name': self._name}
        dictOutput = json.loads(description)
        return dictOutput
