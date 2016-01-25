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
import os.path
from subprocess import PIPE, Popen
from threading  import Thread
from tempfile import NamedTemporaryFile, mkdtemp

from opencmiss.neon.core.simulations.local import LocalSimulation
from opencmiss.neon.core.serialisers.identifiervalue import IdentifierValue
from opencmiss.neon.settings.mainsettings import EXTERNAL_DATA_DIR

try:
    from Queue import Queue
except ImportError:
    from queue import Queue  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


class Ventilation(LocalSimulation):

    def __init__(self):
        super(Ventilation, self).__init__()
        self.setName('Ventilation Simulation')
        self.setSerialiser(IdentifierValue())
        self._file_handles = {}
        self._dir_handles = {}
        self._output_filename = ''

    def getOutputFilename(self):
        return self._output_filename

    def setup(self):
        file_input_outputs = self._parameters['file_input_outputs']

        out_file = file_input_outputs['out_exnode']
        if not out_file:
            out_file_handle = NamedTemporaryFile(prefix='ventilation_out_', suffix='.exnode', delete=False)
            out_file = out_file_handle.name
            out_file_handle.close()

        inbuilt_flow_exelem = os.path.join(EXTERNAL_DATA_DIR, self._parameters['name'], 'Geom', 'FlowLarge.exelem')
        flow_exelem = inbuilt_flow_exelem if file_input_outputs['flow_inbuilt'] or not file_input_outputs['flow_exelem'] else file_input_outputs['flow_exelem']

        self._dir_handles['root'] = mkdtemp(prefix='neon_')
        param_dir = os.path.join(self._dir_handles['root'], 'Parameters')
        self._dir_handles['para'] = param_dir
        os.mkdir(param_dir)

        geometry_flow = {}
        geometry_flow['exnode'] = "'{0}'".format(out_file)
        geometry_flow['exelem'] = "'{0}'".format(flow_exelem)
        self._file_handles['geo_main'] = os.path.join(self._dir_handles['para'], 'geometry_evaluate_flow.txt')
        with open(self._file_handles['geo_main'], 'w') as f:
            string = self._serialiser.serialise(geometry_flow)
            f.write(string)

        self._output_filename = out_file

        inbuilt_tree_ipelem = os.path.join(EXTERNAL_DATA_DIR, self._parameters['name'], 'Geom', 'tree.ipelem')
        tree_ipelem = inbuilt_tree_ipelem if file_input_outputs['tree_inbuilt'] or not file_input_outputs['tree_ipelem'] else file_input_outputs['tree_ipelem']
        inbuilt_tree_ipnode = os.path.join(EXTERNAL_DATA_DIR, self._parameters['name'], 'Geom', 'tree.ipnode')
        tree_ipnode = inbuilt_tree_ipnode if file_input_outputs['tree_inbuilt'] or not file_input_outputs['tree_ipnode'] else file_input_outputs['tree_ipnode']
        inbuilt_tree_ipfiel = os.path.join(EXTERNAL_DATA_DIR, self._parameters['name'], 'Geom', 'tree.ipfiel')
        tree_ipfiel = inbuilt_tree_ipfiel if file_input_outputs['tree_inbuilt'] or not file_input_outputs['tree_ipfield'] else file_input_outputs['tree_ipfield']
        inbuilt_tree_exnode = os.path.join(EXTERNAL_DATA_DIR, self._parameters['name'], 'Geom', 'tree.exnode')
        tree_exnode = inbuilt_tree_exnode if file_input_outputs['tree_inbuilt'] or not file_input_outputs['tree_exnode'] else file_input_outputs['tree_exnode']
        inbuilt_tree_exelem = os.path.join(EXTERNAL_DATA_DIR, self._parameters['name'], 'Geom', 'tree.exelem')
        tree_exelem = inbuilt_tree_exelem if file_input_outputs['tree_inbuilt'] or not file_input_outputs['tree_exelem'] else file_input_outputs['tree_exelem']

        geometry_main = {}
        geometry_main['ipelem'] = "'{0}'".format(tree_ipelem)
        geometry_main['ipnode'] = "'{0}'".format(tree_ipnode)
        geometry_main['ipfiel'] = "'{0}'".format(tree_ipfiel)
        geometry_main['exnode'] = "'{0}'".format(tree_exnode)
        geometry_main['exelem'] = "'{0}'".format(tree_exelem)

        self._file_handles['geo_flow'] = os.path.join(self._dir_handles['para'], 'geometry_main.txt')
        with open(self._file_handles['geo_flow'], 'w') as f:
            string = self._serialiser.serialise(geometry_main)
            f.write(string)

        self._file_handles['par_main'] = os.path.join(self._dir_handles['para'], 'control_params_main.txt')
        with open(self._file_handles['par_main'], 'w') as f:
            string = self._serialiser.serialise(self._parameters['main_parameters'])
            f.write(string)

        self._file_handles['par_flow'] = os.path.join(self._dir_handles['para'], 'params_evaluate_flow.txt')
        with open(self._file_handles['par_flow'], 'w') as f:
            string = self._serialiser.serialise(self._parameters['flow_parameters'])
            f.write(string)

    def execute(self):
        p = Popen([self._executable], cwd=self._dir_handles['root'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
        q = Queue()
        t = Thread(target=enqueue_output, args=(p.stdout, q))
        t.daemon = True  # thread dies with the program
        t.start()

        return t, q

    def cleanup(self):
        os.remove(self._file_handles['geo_main'])
        os.remove(self._file_handles['geo_flow'])
        os.remove(self._file_handles['par_main'])
        os.remove(self._file_handles['par_flow'])
        os.rmdir(self._dir_handles['para'])
        os.rmdir(self._dir_handles['root'])

    def validate(self):
        return True
