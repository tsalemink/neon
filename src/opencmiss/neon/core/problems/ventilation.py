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
import sys

from opencmiss.neon.core.problems.external import ExternalProblem
import json


def getExecutableForPlatform():
    return 'ventilation-' + sys.platform


class Ventilation(ExternalProblem):

    def __init__(self):
        super(Ventilation, self).__init__()
        self.setName('Ventilation')
        self.setInBuiltExecutable(getExecutableForPlatform())

        self._file_input_outputs = self._defineDefaultFileInputOutputs()
        self._main_parameters = self._defineDefaultMainParameters()
        self._flow_parameters = self._defineDefaultFlowParameters()

    def _defineDefaultMainParameters(self):
        d = {}
        d['num_brths'] = 5
        d['num_itns'] = 200
        d['dt'] = 0.05
        d['err_tol'] = 1e-10

        return d

    def _defineDefaultFlowParameters(self):
        d = {}
        d['FRC'] = 0.36000E+01
        d['constrict'] = 1.00000E+00
        d['T_interval'] = 4.00000E+00
        d['Gdirn'] = 3
        d['press_in'] = 0.00000E+00
        d['COV'] = 0.20000E+00
        d['RMaxMean'] = 1.29000E+00
        d['RMinMean'] = 0.78000E+00
        d['i_to_e_ratio'] = 0.5000E+00
        d['refvol'] = 0.60000E+00
        d['volume_target'] = 8.00000E+05
        d['pmus_step'] = -5.29559E+02
        d['expiration_type'] = 'passive'
        d['chest_wall_compliance'] = 2039.4324E+00

        return d

    def _defineDefaultFileInputOutputs(self):
        d = {}
        d['tree_inbuilt'] = True
        d['tree_ipelem'] = ''
        d['tree_ipnode'] = ''
        d['tree_ipfield'] = ''
        d['tree_exnode'] = ''
        d['tree_exelem'] = ''

        d['flow_inbuilt'] = True
        d['flow_exelem'] = ''

        d['out_exnode'] = ''

        return d

    def getFileInputOutputs(self):
        return self._file_input_outputs

    def getMainParameters(self):
        return self._main_parameters

    def getFlowParameters(self):
        return self._flow_parameters

    def updateMainParameters(self, parameters):
        self._main_parameters.update(parameters)

    def updateFlowParameters(self, parameters):
        self._flow_parameters.update(parameters)

    def updateFileInputOutputs(self, values):
        self._file_input_outputs.update(values)

    def serialise(self):
        d = {}
        d['executable_inbuilt'] = self.isInBuiltExecutable()
        d['executable'] = self.getExecutable() if not self.isInBuiltExecutable() else ''
        d['file_input_outputs'] = self._file_input_outputs
        d['main_parameters'] = self._main_parameters
        d['flow_parameters'] = self._flow_parameters
        return json.dumps(d)

    def deserialise(self, string):
        d = json.loads(string)
        executable_inbuilt = d['executable_inbuilt'] if 'executable_inbuilt' in d else True
        if executable_inbuilt:
            self.setInBuiltExecutable(getExecutableForPlatform())
        else:
            self.setExecutable(d['executable'] if 'executable' in d else '')
        self._file_input_outputs = d['file_input_outputs'] if 'file_input_outputs' in d else self._defineDefaultFileInputOutputs()
        self._main_parameters = d['main_parameters'] if 'main_parameters' in d else self._defineDefaultMainParameters()
        self._flow_parameters = d['flow_parameters'] if 'flow_parameters' in d else self._defineDefaultFlowParameters()

    def validate(self):
        return True
