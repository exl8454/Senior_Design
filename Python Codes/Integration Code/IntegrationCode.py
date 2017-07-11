import spidev
import os
import time
from time import sleep
from datetime import datetime

spi=spidev.SpiDev()
spi.open(0,0)

#Sensor Location
ang0chan=0
sampletime=1/2

#Potentiometer Functions
def getReading(channel):
	rawPdata=spi.xfer([1,(8+channel) << 4,0])
	processedPdata=((rawPdata[1]&3) << 8) +rawPdata[2]
	return processedPdata

def convertDegree(bitValue, decimalPlaces=6):
	#Converts to degrees ranging from 0-340
	phiDegree=(bitValue*340)/float(1023)
	phiDegree=round(phiDegree,decimalPlaces)
	return phiDegree

file = open("/home/edward/Desktop/LIDAR_data1.csv", "a")

if os.stat("/home/edward/Desktop/LIDAR_data1.csv").st_size == 0:
        file.write("Time, Angle \n")

#Later install switch to controll recording
while True:
        now = datetime.now()
        angData=getReading(ang0chan)
        Angle=convertDegree(angData)

        #Collect data from LIDAR        
        file.write(str(now)+" , "+str(Angle)+"\n")
        file.flush()
        print("Time = {} , Angle = {}".format(now, Angle))
        time.sleep(steptime)

    sleep(sampletime)





