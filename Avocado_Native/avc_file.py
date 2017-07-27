# avc_file.py
# File handler

# Native Imports
import os
import os.path
import time
from datetime import datetime

# Third-Party Imports

# Avocado Imports
from avc_logger import AvcLogger as Logger
from avc_data import AvcData as DataLogger

class AvcFile(object):
    logger = None
    data = None

    def __init__(self, logger, data):
        self.logger = logger
        self.data = data
        return
    
    # Force closes all files
    def closeAll():
        self.logger.close()
        self.data.close()
        return

    # Closes only dump file
    def closeDump():
        self.logger.close()
        return

    # Closes only data file
    def closeData():
        self.data.close()
        return

    # Dump Related
    def writeDump(self, line, title = "DMP", timestamp = True, append = False):
        self.logger.writeTo(line, title, timestamp, append)
        return

    def writeInfo(self, line):
        self.logger.writeTo(line, "INF")
        return

    def writeLog(self, line):
        self.logger.writeTo(line, "LOG")
        return

    def writeErr(self, line):
        self.logger.writeTo(line, "ERR")
        return

    def writeDat(self, line):
        self.logger.writeTo(line, "DAT")
        return

    # Data Related
    def writeData(self, args):
        self.data.writeTo(args)
        return
