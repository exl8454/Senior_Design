# avc_file.py
# File handler

# Native Imports
import os
import os.path
import time
from datetime import datetime

class FileHandler(object):
    # Variables
    fileCount = 0
    dumpLoc = ""
    dataLoc = ""
    fileLoc = ["", ""]
    
    dumpFile = None
    dataFile = None
    files = [None, None]

    openFile = None
    
    # Force closes all files
    def CloseAll():
        self.files[0].close()
        self.files[1].close()

    # Closes only dump file
    def CloseDump():
        self.files[0].close()

    # Closes only data file
    def CloseData():
        self.files[1].close()

    def CreateFile(name, config):
        if os.path.isFile(name):
            return None
        else:
            return open(name, config)

    def OpenFile(loc):
        global openFile
        if not(openFile is None) and not(openFile.closed):
            openFile.close()

        try:
            openFile = open(loc, "r")
            return openFile
        except IOError as ioe:
            WriteErr("\/Encountered error while opening file\/")
            WriteErr(ioe)
            return None

    # Initializes files
    # Provide Directory to save data and dump
    def InitFiles(directory):
        self.fileCount = 0
        self.dumpLoc = directory + "/LIDAR_DUMP" + str(self.fileCount) + ".txt"
        self.dataLoc = directory + "/LIDAR_DATA" + str(self.fileCount) + ".csv"

        # Files first
        while(os.path.isfile(self.dataLoc)):
            self.fileCount += 1
            self.dumpLoc = directory + "/LIDAR_DUMP" + str(self.fileCount) + ".txt"
            self.dataLoc = directory + "/LIDAR_DATA" + str(self.fileCount) + ".csv"

        self.fileLoc[0] = self.dumpLoc
        self.fileLoc[1] = self.dataLoc

        self.dumpFile = open(self.fileLoc[0], "w")
        self.dataFile = open(self.fileLoc[1], "w")

        self.files[0] = self.dumpFile
        self.files[1] = self.dataFile
        
    # WriteTo function writes to file. If append parameter is left false,
    # function will force set \n character at the end.
    # If fileType parameter is left as 0, function will write to dump file as default.
    # If title parameter is not set, it will also send default expression.
    # Anything in line will forced converted to string type.
    def WriteTo(line, fileType = 0, title = "DMP", append = False, timestamp = True):
        # Open file if it is closed
        if self.files[fileType].closed:
            self.files[fileType] = open(self.fileLoc[fileType], "a")
        # End
        # Write to file
        if timestamp: # If timestamp is true, timestamp will be added
            self.files[fileType].write("[ " + str(datetime.now()) + " ]")
            
        # Otherwise will print title and data
        self.files[fileType].write("[ " + title + " ]:" + str(line))
        
        if not(append):
            self.files[fileType].write("\n")
        self.files[fileType].close()

    def WriteInfo(line, append = False):
        WriteTo(line, 0, "INF", append, timestamp = True)

    def WriteLog(line, append = False):
        WriteTo(line, 0, "LOG", append, timestamp = True)

    def WriteErr(line, append = False):
        WriteTo(line, 0, "ERR", append, timestamp = True)

    def WriteData(line, append = False):
        WriteTo(line, 0, "DAT", append, timestamp = False)

    def Write(line, append = False):
        if self.files[fileType].closed:
            self.files[fileType] = open(self.fileLoc[fileType], "a")
        self.files[1].write(line);
        if not(append):
            self.files[1].write("\n")
        self.files[1].close()
