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
from functools import partial

logErrorMessage = 0
logWarningMessage = 0
logInformationMessage = 0
    
def logsDialogErrorMessage(logsDialog, message):
    if logsDialog:
        logsDialog.writeErrorMessage(message)
    else:
        print "Error: " +  message
    
def logsDialogWarningMessage(logsDialog, message):
    if logsDialog:
        logsDialog.writeWarningMessage(message)
    else:
        print "Warning: " +  message
    
def logsDialogInformationMessage(logsDialog, message):
    if logsDialog:
        logsDialog.writeInformationMessage(message)
    else:
        print "Information: " +  message

def setGlobalLogsMessage(logsDialog):
    global logErrorMessage
    global logWarningMessage
    global logInformationMessage
    if logsDialog:
        logErrorMessage = partial(logsDialogErrorMessage, logsDialog)
        logWarningMessage = partial(logsDialogWarningMessage, logsDialog)
        logInformationMessage = partial(logsDialogInformationMessage, logsDialog)