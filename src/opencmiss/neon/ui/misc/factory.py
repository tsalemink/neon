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


def instantiateRelatedClasses(model, view):
    classes = []
    for row in range(model.rowCount()):
        problem = model.getProblem(row)
        module = problem.__module__.replace('core.problems', 'ui.' + view)
        name = problem.__class__.__name__

        module_name = importlib.import_module(module)
        class_ = getattr(module_name, name)
        classes.append(class_())

    return classes
