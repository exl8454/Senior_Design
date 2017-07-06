import os
import os.path
import subprocess
import spidev
import time
from time import sleep
from datetime import datetime
import threading

class SubProc(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            global startTime
            global endTime
            global mainWorking
            endTime = int(round(time.time() * 1000))
            if (endTime - startTime) >= sampleRate and not(mainWorking) :
                getData()
                writeData()
                startTime = endTime
                mainWorking = True
    
def getData(channel = 0, decimalPlaces = 6):
    global proc
    global isValid
    outputline = proc.stdout.readline()
    parsed = str(outputline, 'utf-8')
    splits = parsed.split(": : ")
    if len(splits) > 1: # Python will only parse the data when it has full data
        rawPdata=spi.xfer([1,(8+channel) << 4 , 0])
        processedPdata=((rawPdata[1]&3) << 8) +rawPdata[2]
            
        #Converts to degrees ranging from 0-340
        global angle
        angle=(processedPdata * 340) / float(1023)
        angle=round(angle, decimalPlaces)
        
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

def writeData():
    global lidarOutput
    global isValid
    if isValid:
        now = datetime.now()
        file.write(str(now)+","+str(angle)+ lidarOutput + "\n")
        file.flush()
        isValid = False
    

# Thread handler
mainWorking = True

# Data vailidty checker
isValid = False

# RPI bash start
proc = subprocess.Popen('./runpy-2.sh', bufsize = -1, stdout = subprocess.PIPE)

# ADC SPI
spi = spidev.SpiDev()
spi.open(0, 0)

# Pot Data
angle = 0;

# RPLidar Data
timestamp = "inf" #timestamp for Lidar
lidarAngle = "inf" # Lidar angle
lidarDist = "inf" # Lidar distance
lidarOutput = "inf" # Used to combine all

sampleRate = 10 # As in milliseconds

# For state machine
startTime = 0
endTime = 0

# New file generator
fileCount = 0;
fileName = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + ".csv"

while(os.path.isfile(fileName)):
    fileCount += 1 ;
    fileName = "/home/edward/Desktop/LIDARDUMP/LIDAR_data" + str(fileCount) + ".csv"

print ("Created new file " + fileName) # Reports new file name

file = open(fileName, "w") # overwrite existing file, otherwise create one
file.write("Time,Angle,TIME,ANGL,DIST\n")

subThread = SubProc()
subThread.start()

print ("ctrl+c to stop")

#Later install switch to controll recording
while True:
    endTime = int(round(time.time() * 1000))
    if (endTime - startTime) >= sampleRate and mainWorking :
        getData()
        writeData()
        startTime = endTime
        mainWorking = False

#After loop
