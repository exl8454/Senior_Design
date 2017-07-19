# AvocadoLogger.py
# For printing to screen + Writing to dump file

# Native Imports
import os
from datetime import datetime

# Prints to Python shell
def printTo(line, title = "DMP", timestamp = True):
    pack = ""
    if timestamp:
        pack += "[" + str(datetime.now()) + "]"
    pack += "[  " + title + "  ]"
    pack += str(line)
    print (pack)
    return

def printInfo(line):
    printTo(line, "INF")
    return

def printLog(line):
    printTo(line, "LOG")
    return

def printErr(line):
    printTo(line, "ERR")
    return

def printDat(line):
    printTo(line, "DAT")
    return

# Use this for file handling
class Avocado_Logger(object):
    directory = "AVC_DATA/AVC_DUMP_0.txt"  # File directory
    _file = None     # File object
    def __init__(self, directory, option = "w"):
        self.directory = directory
        self._file = open(self.directory, option)
        
    # Writes to target file
    def writeTo(self, line, title = "DMP", timestamp = True, append = False):
        if self._file.closed:
            self._file = open(directory, "a")
            
        if timestamp:
            self._file.write("[" + str(datetime.now()) + "]")
        self._file.write("[  " + title + "  ]")
        self._file.write(str(line))

        if not append:
            self._file.write("\n")

        self._file.close()
        return

    def writeInfo(self, line):
        writeTo(line, "INF")
        return

    def writeLog(self, line):
        writeTo(line, "LOG")
        return

    def writeErr(self, line):
        writeTo(line, "ERR")
        return

    def writeDat(self, line):
        writeTo(line, "DAT")
        return
