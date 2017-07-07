# RPLidar Module
# Handles PRLidar Launching module

import os
import os.path
import subprocess
import spidev
import time
from time import sleep
from datetime import datetime
import threading

class InitProcess(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self): # send dump, not data
        global dumpFile, dumpLoc, dataFile, dataLoc
        global initProcess
        if not(dumpFile.closed):
            dumpFile.close()
            dumpFile = open(dumpLoc, "a")
        else:
            dumpFile = open(dumpLoc, "a")
        # Should start writing to dump file
        # Starts ROS initialization
        initProcess = subprocess.Popen('./runpy-1.sh', stdout = subprocess.PIPE)
        for line in initProcess.stdout:
            dumpFile.write(str(datetime.now()) + " Init Process: " + str(line) + "\n")
        
class ScanProcess(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global dumpFile, dumpLoc, dataFile, dataLoc
        global scanProcess
        while True:
            getData()
            writeData()
                
def getData(channel = 0, decimalPlaces = 6):
    global dumpLoc, dumpFile, dataLoc, dataFile
    global scanProcess
    global isValid
    
    if not(dumpFile.closed):
        dumpFile.close()
        dumpFile = open(dumpLoc, "a")
    else:
        dumpFile = open(dumpLoc, "a")
    if not(dataFile.close):
        dataFile.close()
        dataFile = open(dataLoc, "a")
    else:
        dataFile = open(dataLoc, "a")
                    
    outputline = scanProcess.stdout.readline()
    parsed = str(outputline, 'utf-8')
    splits = parsed.split(": : ")
    if len(splits) > 1:
        rawPdata = spi.xfer([1, (8 + channel) << 4, 0])
        processedPdata = ((rawPdata[1] & 3) << 8) + rawPdata[2]

        global angle
        angle = (processedPdata * 340) / float(1023)
        angle = round(angle, decimalPlaces)

        try:
            global timestamp
            timestamp = splits[0].split("\x1b[0m[ INFO] [")[1].split(']')[0]
        except IndexError:
            print ("Index Error Received, Data was ", splits)
        angledist = splits[1].split("\x1b[0m\n")
        global lidarAngle
        lidarAngle = angledist[0].split("[")[1].split(",")[0]
        global lidarDist
        lidarDist = angledist[0].split(",")[1].split("]")[0]
        global lidarOutput
        lidarOutput = ",TIME = " + timestamp + ",ANGL = " + lidarAngle + ",DIST = " + lidarDist
        isValid = True
    else:
        dumpFile.write(str(datetime.now()) + " Malformed Data: " + parsed + "\n")

def writeData():
    global dumpLoc, dumpFile, dataLoc, dataFile
    global lidarOutput
    global isValid

    if not(dumpFile.closed):
        dumpFile.close()
        dumpFile = open(dumpLoc, "a")
    else:
        dumpFile = open(dumpLoc, "a")
    if not(dataFile.close):
        dataFile.close()
        dataFile = open(dataLoc, "a")
    else:
        dataFile = open(dataLoc, "a")
            
    if isValid:
        now = datetime.now()
        dataFile.write(str(now) + "," + str(angle) + lidarOutput + "\n")
        dataFile.flush()
        isValid = False

# Variables
initProcess = None
scanProcess = None

mainWorking = True # For thread handling
isValid = False # For data validity

# ADC SPI
spi = spidev.SpiDev()
spi.open(0, 0)

angle = 0 # Potentiometer angle report

# RPLidar Data
timestamp = "inf" #timestamp for Lidar
lidarAngle = "inf" # Lidar angle
lidarDist = "inf" # Lidar distance
lidarOutput = "inf" # Used to combine all

initProc = InitProcess() # InitProc thread will initialize RPLidar to use
scanProc = ScanProcess() # ScanProc thread will handle data from potentiometer and LIDAR

fileCount = 0
dumpLoc = "/home/edward/Desktop/LIDARDUMP/LIDAR_dump" + str(fileCount) + ".txt"
dataLoc = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + ".csv"

# Files first
while(os.path.isfile(dataLoc)):
    fileCount += 1
    dumpLoc = "/home/edward/Desktop/LIDARDUMP/LIDAR_dump" + str(fileCount) + ".txt"
    dataLoc = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + ".csv"

dumpFile = open(dumpLoc, "w") # Used to dump EVERYTHING
dataFile = open(dataLoc, "w") # Used to save all proper data

scanProcess = subprocess.Popen('./runpy-2.sh', bufsize = -1, stdout = subprocess.PIPE)
    
# Start initProc first
initProc.start()
scanProc.start()

# Start reading
initProc.join()
scanProc.join()
