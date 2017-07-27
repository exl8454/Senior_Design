# avc_logger.py
# Logger Object (Not for data writing!)

# Native Imports
import os
import os.path
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

class AvcLogger(object):
    directory = ""  # File directory
    _file = None     # File object
    
    def __init__(self, directory, filecount, option = "w"):
        self.directory = directory + "/DUMP_" + str(datetime.today().date()) + "_" + str(filecount) + ".txt"

        while os.path.isfile(self.directory):
            filecount += 1
            self.directory = directory + "/DUMP_" + str(datetime.today().date()) + "_" + str(filecount) + ".txt"
        
        self._file = open(self.directory, option)

        return

    def close(self):
        if not self._file.closed:
            self._file.close()
            pass
        return
        
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
