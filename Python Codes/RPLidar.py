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

    def run(self, dumpFile, dumpLoc): # send dump, not data
        if not(dumpFile.closed):
            dumpFile.close() # Release from previous one
        dumpFile = open(fileLoc, "a")
        # Should start writing to dump file
        dumpFile.write("InitProcess: Initiating ROS")
        # Starts ROS initialization
        process = subprocess.Popen('./runpy-1.sh', stdout = subprocess.PIPE)
        for line in stdout:
            dumpFile.write("InitProcess: " + str(line))
        dumpFile.close() # This might not work since shell script will keep run

class ScanProcess(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self, dumpFile, dataFile, dumpLoc, dataLoc):
        global mainWorking
        while True:
            if not(dumpFile.closed):
                dumpFile.close()
                dumpFile = open(dumpLoc, "a")
            if not(dataFile.close):
                dataFile.close()
                dataFile = open(dataLoc, "a")

           getData()
           writeData()

class RPLidarData(object):

    timestamp = "inf"
    lidarAngle = "inf"
    lidarDist = "inf"
    lidarOutput = "inf"

    def output(time, angle, dist):
        lidarOutput = "," + time + " = " + timestamp + "," + angle + " = " + lidarAngle + "," + dist + " = " + lidarDist
        
                
def getData(channel = 0, decimalPlace = 6):
    global process
    global isValid
    outputline = process.stdout.readline()
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
        global dumpFile
        dumpFile.write("Malformed Data: ", parsed)

def writeData():
    global lidarOutput
    global isValid
    if isValid:
        now = datetime.now()
        file.write(str(now) + "," + str(angle) + lidarOutput + "\n")
        file.flush()
        isValid = False

# Variables
mainWorking = True # For thread handling
isValid = False # For data validity

spi = spidev.SpiDev()
spi.open(0, 0)

angle = 0 # Potentiometer angle report

fileCount = 0
fileName = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + ".csv"

while(os.path.isfile(fileName)):
    fileCount += 1 ;
    fileName = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + ".csv"

dumpLoc = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + "_dump.txt"
dataLoc = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + ".csv"
