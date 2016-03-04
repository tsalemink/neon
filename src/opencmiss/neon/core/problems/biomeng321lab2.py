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

from opencmiss.neon.core.problems.base import BaseProblem

BOUNDARY_CONDITIONS = ['Model 1 (Equibiaxial extension of unit cube, isotropic, 0 degree fibre rotation)',
    'Model 2 (Equibiaxial extension of unit cube, orthotropic, 0 degree fibre rotation)',
    'Model 3 (Equibiaxial extension of unit cube, isotropic, 30 degree fibre rotation)',
    'Model 4 (Equibiaxial extension of unit cube, isotropic, 45 degree fibre rotation)',
    'Model 5 (Equibiaxial extension of unit cube, orthotropic, 45 degree fibre rotation)',
    'Model 6 (Equibiaxial extension of unit cube, orthotropic, 90 degree fibre rotation)']


class Biomeng321Lab2(BaseProblem):

    def __init__(self):
        super(Biomeng321Lab2, self).__init__()
        self.setName('Biomeng321 Lab2')
        self._boundary_condition = None

    def setBoundaryCondition(self, boundary_condition):
        self._boundary_condition = boundary_condition

    def getBoundaryCondition(self):
        return self._boundary_condition

    def serialize(self):
        d = {}
        d['boundary_condition'] = self._boundary_condition

        return json.dumps(d)

    def deserialize(self, string):
        d = json.loads(string)
        self._boundary_condition = d['boundary_condition'] if 'boundary_condition' in d else BOUNDARY_CONDITIONS[0]

    def validate(self):
        return True
