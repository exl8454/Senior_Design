# StreamHandler.py
# Handles data input and output

import os
import os.path
import time
from datetime import datetime

# Initializes files
# Provide Directory to save data and dump
def InitFiles(directory):
    global fileCount, dumpLoc, dataLoc, fileLoc, dumpFile, dataFile, files
    fileCount = 0
    dumpLoc = directory + "/LIDAR_DUMP" + str(fileCount) + ".txt"
    dataLoc = directory + "/LIDAR_DATA" + str(fileCount) + ".csv"

    # Files first
    while(os.path.isfile(dataLoc)):
        fileCount += 1
        dumpLoc = directory + "/LIDAR_DUMP" + str(fileCount) + ".txt"
        dataLoc = directory + "/LIDAR_DATA" + str(fileCount) + ".csv"

    fileLoc[0] = dumpLoc
    fileLoc[1] = dataLoc

    dumpFile = open(fileLoc[0], "w")
    dataFile = open(fileLoc[1], "w")

    files[0] = dumpFile
    files[1] = dataFile
    
# WriteTo function writes to file. If append parameter is left false,
# function will force set \n character at the end.
# If fileType parameter is left as 0, function will write to dump file
# as default.
# If title parameter is not set, it will also send default expression.
# Anything in line will forced converted to string type.
def WriteTo(line, fileType = 0, title = " DUMP=", append = False, timestamp = True):
    global fileLoc, files
    # Open file if it is closed
    if files[fileType].closed:
        files[fileType] = open(fileLoc[fileType], "a")
    # End
    # Write to file
    if timestamp: # If timestamp is true, timestamp will be added
        files[fileType].write(str(datetime.now()) + "\n")
    # Otherwise will print title and data
    files[fileType].write(title + str(line))
    
    if not(append):
        files[fileType].write("\n")
    files[fileType].close()

def WriteLog(line, append = False):
    WriteTo(line, 0, " Log: ", append, timestamp = True)

def WriteErr(line, append = False):
    WriteTo(line, 0, " Error: ", append, timestamp = True)

def WriteData(line, append = False):
    WriteTo(line, 0, " Data: ", append, timestamp = True)

def Write(line, append = False):
    WriteTo(line, 1, "", append, timestamp = False)

fileCount = 0
dumpLoc = ""
dataLoc = ""

fileLoc = ["", ""]
dumpFile = None
dataFile = None

files = [None, None]
