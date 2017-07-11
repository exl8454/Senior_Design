# StreamHandler.py
# Handles data input and output

import os
import os.path
import time
from datetime import datetime

# Force closes all files
def CloseAll():
    files[0].close()
    files[1].close()

def CloseDump():
    files[0].close()

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
    
# WriteTo function writes to file. If append parameter is left false,
# function will force set \n character at the end.
# If fileType parameter is left as 0, function will write to dump file
# as default.
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

def WriteLog(line, append = False):
    WriteTo(line, 0, "[  LOG  ]: ", append, timestamp = True)

def WriteErr(line, append = False):
    WriteTo(line, 0, "[  ERR  ]: ", append, timestamp = True)

def WriteData(line, append = False):
    WriteTo(line, 0, "[  DAT  ]: ", append, timestamp = False)

def Write(line, append = False):
    WriteTo(line, 1, "", append, timestamp = False)

def PrintTo(line, title = "DUMP"):
    print ("[ " + str(datetime.now()) + " ]" + "[  " + title + "  ]: " + str(line))

def OpenFile(loc):
    global openFile
    if not(openFile is None) and not(openFile.closed):
        openFile.close()

    try:
        openFile = open(loc, "r")
        return 0
    except IOError as ioe:
        PrintTo(str(ioe), "ERR")
        return -1

def ReadConfig():
    global openFile
    status = OpenFile("config.avocado")
    if status != 0:
        PrintTo("Avocado didn't detect its configuration file!", "ERR")
        PrintTo("Auto-generating default configuration...", "INFO")
        openFile = open("config.avocado", "w")
        openFile.write("avocado_dump_data=False\n")
        openFile.write("avocado_read_interval=10\n")
        openFile.write("avocado_lidar_scan_type=0\n")
        openFile.write("avocado_servo_interval=15\n")
        openFile.write("avocado_serial_timeout=5\n")
        openFile.close()
        return -1
    else:
        PrintTo("Config file loaded, changing settings...", "INFO")
        line = openFile.read()
        line = line.split("\n")
        avocado_dump_data = line[0].split("=")[1] in ['True', 'False']
        avocado_read_interval = int(line[1].split("=")[1])
        avocado_lidar_scan_type = int(line[2].split("=")[1])
        avocado_servo_interval = int(line[3].split("=")[1])
        avocado_serial_timeout = int(line[3].split("=")[1])
        return [avocado_dump_data,
                avocado_read_interval,
                avocado_lidar_scan_type,
                avocado_servo_interval,
                avocado_serial_timeout]
        openFile.close()

fileCount = 0
dumpLoc = ""
dataLoc = ""

fileLoc = ["", ""]
dumpFile = None
dataFile = None

openFile = None

files = [None, None]
