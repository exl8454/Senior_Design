# StreamHandler.py
# Handles data input and output

# Native imports
import os
import os.path
import time
from datetime import datetime

# Force closes all files
def CloseAll():
    files[0].close()
    files[1].close()

# Closes only dump file
def CloseDump():
    files[0].close()

# Closes only data file
def CloseData():
    files[1].close()

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

def CreateFile(name, config):
    if os.path.isFile(name):
        return None
    else:
        return open(name, config)
    
# WriteTo function writes to file. If append parameter is left false,
# function will force set \n character at the end.
# If fileType parameter is left as 0, function will write to dump file as default.
# If title parameter is not set, it will also send default expression.
# Anything in line will forced converted to string type.
def WriteTo(line, fileType = 0, title = "[  DMP  ]: ", append = False, timestamp = True):
    global fileLoc, files
    # Open file if it is closed
    if files[fileType].closed:
        files[fileType] = open(fileLoc[fileType], "a")
    # End
    # Write to file
    if timestamp: # If timestamp is true, timestamp will be added
        files[fileType].write("[ " + str(datetime.now()) + " ]")
        
    # Otherwise will print title and data
    files[fileType].write(title + str(line))
    
    if not(append):
        files[fileType].write("\n")
    files[fileType].close()

def WriteInfo(line, append = False):
    WriteTo(line, 0, "[  INF  ]: ", append, timestamp = True)

def WriteLog(line, append = False):
    WriteTo(line, 0, "[  LOG  ]: ", append, timestamp = True)

def WriteErr(line, append = False):
    WriteTo(line, 0, "[  ERR  ]: ", append, timestamp = True)

def WriteData(line, append = False):
    WriteTo(line, 0, "[  DAT  ]: ", append, timestamp = False)

def Write(line, append = False):
    WriteTo(line, 1, "", append, timestamp = False)

def PrintTo(line, title = "DMP"):
    print ("[ " + str(datetime.now()) + " ]" + "[  " + title + "  ]: " + str(line))

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

# Variables
fileCount = 0
dumpLoc = ""
dataLoc = ""

fileLoc = ["", ""]
dumpFile = None
dataFile = None

openFile = None

files = [None, None]
