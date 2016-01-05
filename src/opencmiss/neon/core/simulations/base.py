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


class BaseSimulation(object):

    def __init__(self):
        self._name = 'Base'
        self._parameters = {}

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def setParameters(self, parameters):
        self._parameters = parameters

    def setup(self):
        raise NotImplementedError()

    def execute(self):
        raise NotImplementedError()

    def cleanup(self):
        raise NotImplementedError()
