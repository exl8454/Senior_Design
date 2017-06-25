import spidev
from time import sleep
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

while True:
    angData=getReading(ang0chan)
    Angle=convertDegree(angData)

    #Display
    print("Angle bitValue = {} ; Angle Degrees = {}".format(angData, Angle))

    sleep(sampletime)





