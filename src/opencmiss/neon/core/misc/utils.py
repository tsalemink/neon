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
import importlib


def importProblem(name):
    module_name = importlib.import_module('.' + name.lower(), 'opencmiss.neon.core.problems')
    class_ = getattr(module_name, name)

    return class_()


def getMatchingVisualisationClass(simulation):
    module_string = simulation.__class__.__module__
    class_name = simulation.__class__.__name__
    visualisation_module = module_string.replace('simulations', 'visualisations')
    module_name = importlib.import_module(visualisation_module)
    class_ = getattr(module_name, class_name)

    return class_()
