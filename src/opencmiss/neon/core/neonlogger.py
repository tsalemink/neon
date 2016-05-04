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

ENABLE_STD_STREAM_CAPTURE = True


class CustomStreamImpl(QtCore.QObject):
    # Signal is a class variable; PySide creates per-instance SignalInstance object of same name
    messageWritten = QtCore.Signal(str, str)

    # Note: if implementing __init__ you must call super __init__ for Signals to work.
    # def __init__(self):
    #     super(CustomStreamImpl, self).__init__()

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg, level="INFORMATION"):
        if (not self.signalsBlocked()):
            self.messageWritten.emit(msg, level)


class CustomStream(object):
    _stdout = None
    _stderr = None

    @staticmethod
    def stdout():
        if CustomStream._stdout is None:
            CustomStream._stdout = CustomStreamImpl()
            if ENABLE_STD_STREAM_CAPTURE:
                sys.stdout = CustomStream._stdout
        return CustomStream._stdout

    @staticmethod
    def stderr():
        if CustomStream._stderr is None:
            CustomStream._stderr = CustomStreamImpl()
            if ENABLE_STD_STREAM_CAPTURE:
                sys.stderr = CustomStream._stderr
        return CustomStream._stderr


class LogsToWidgetHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        levelString = record.levelname
        record = self.format(record)
        if record:
            CustomStream.stdout().write('%s\n' % record, levelString)


def setup_custom_logger(name):

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = LogsToWidgetHandler()
    handler.setFormatter(formatter)

    neonLogger = logging.getLogger(name)
    neonLogger.setLevel(logging.DEBUG)
    neonLogger.addHandler(handler)
    return neonLogger


class NeonLogger(object):
    _logger = None
    _zincLogger = None
    _loggerNotifier = None

    @staticmethod
    def getLogger():
        if (not NeonLogger._logger):
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
        NeonLogger.getLogger().info(string)

    @staticmethod
    def loggerCallback(event):
        if event.getChangeFlags() == Logger.CHANGE_FLAG_NEW_MESSAGE:
            text = event.getMessageText()
            if event.getMessageType() == Logger.MESSAGE_TYPE_ERROR:
                NeonLogger.writeErrorMessage(text)
            elif event.getMessageType() == Logger.MESSAGE_TYPE_WARNING:
                NeonLogger.writeWarningMessage(text)
            elif event.getMessageType() == Logger.MESSAGE_TYPE_INFORMATION:
                NeonLogger.writeInformationMessage(text)

    @staticmethod
    def setZincContext(zincContext):
        if NeonLogger._loggerNotifier:
            NeonLogger._loggerNotifier.clearCallback()
        NeonLogger._zincLogger = zincContext.getLogger()
        NeonLogger._loggerNotifier = NeonLogger._zincLogger.createLoggernotifier()
        NeonLogger._loggerNotifier.setCallback(NeonLogger.loggerCallback)
