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
import os.path

from opencmiss.neon.core.problems.base import BaseProblem
from opencmiss.neon.settings.mainsettings import EXTERNAL_BINARIES_DIR


class ExternalProblem(BaseProblem):

    def __init__(self):
        self._executable = ''

    def getExecutable(self):
        return self._executable

    def isInBuiltExecutable(self):
        return self._executable.startswith(EXTERNAL_BINARIES_DIR)

    def setInBuiltExecutable(self, executable):
        self._executable = os.path.join(EXTERNAL_BINARIES_DIR, executable)

    def setExecutable(self, executable):
        self._executable = executable
