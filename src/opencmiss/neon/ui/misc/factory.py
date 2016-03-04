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


def instantiateRelatedClasses(model, view, shared_gl_widget, parent):
    classes = []
    for row in range(model.rowCount()):
        index = model.index(row, 0)
        project = model.getProject(index)
        module = project.__module__.replace('core.neonproject', 'ui.' + view)
        identifier = project.getIdentifier()

        module_name = importlib.import_module(module + '.' + identifier.lower())
        class_ = getattr(module_name, identifier)
        classes.append(class_(shared_gl_widget, parent))

    return classes
