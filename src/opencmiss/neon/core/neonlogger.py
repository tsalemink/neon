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
import logging
from PySide import QtCore
from opencmiss.zinc.logger import Logger

class CustomStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.Signal([str, str])
    
    def flush( self ):
        pass
    
    def fileno( self ):
        return -1
    
    def write( self, msg, level = "INFORMATION"):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(msg, level)
    
    @staticmethod
    def stdout():
        if ( not CustomStream._stdout ):
            CustomStream._stdout = CustomStream()
            sys.stdout = CustomStream._stdout
        return CustomStream._stdout
    
    @staticmethod
    def stderr():
        if ( not CustomStream._stderr ):
            CustomStream._stderr = CustomStream()
            sys.stderr = CustomStream._stderr
        return CustomStream._stderr

class LogsToWidgetHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        levelString = record.levelname
        record = self.format(record)
        if record: CustomStream.stdout().write('%s\n'%record, levelString)

def setup_custom_logger(name):

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = LogsToWidgetHandler()
    handler.setFormatter(formatter)

    neonLogger = logging.getLogger(name)
    neonLogger.setLevel(logging.DEBUG)
    neonLogger.addHandler(handler)
    return neonLogger
    
class NeonLogger():
    _logger = None
    _zincLogger = None
    _loggerNotifier = None
    
    @staticmethod
    def getLogger():
        if ( not NeonLogger._logger ):
            NeonLogger._logger = setup_custom_logger("Neon")
        return NeonLogger._logger

    @staticmethod
    def writeErrorMessage(string):
        NeonLogger.getLogger().error(string)
        
    @staticmethod
    def writeWarningMessage(string):
        NeonLogger.getLogger().warning(string)
    
    @staticmethod
    def writeInformationMessage(string):
        NeonLogger.getLogger().information(string)
    
    @staticmethod
    def loggerCallback(event):
        if event.getChangeFlags() == Logger.CHANGE_FLAG_NEW_MESSAGE:
            if event.getMessageType() == Logger.MESSAGE_TYPE_ERROR:
                NeonLogger.writeErrorMessage(event.getMessageText())
            elif event.getMessageType() == Logger.MESSAGE_TYPE_WARNING:
                NeonLogger.writeWarningMessage(event.getMessageText())
    
    @staticmethod
    def setZincContext(zincContext):
        if NeonLogger._loggerNotifier:
            NeonLogger._loggerNotifier.clearCallback()
        NeonLogger._zincLogger = zincContext.getLogger()
        NeonLogger._loggerNotifier = NeonLogger._zincLogger.createLoggernotifier()
        NeonLogger._loggerNotifier.setCallback(NeonLogger.loggerCallback)
