# avc_servo.py
# Servo Handler with Potentiometer
# Class-object remake

# Native Import
import time

# Thrid-Party Import
import serial

# Custom Import
import StreamHandler as stream
import AvocadoLogger as logger

START = b'avc_start\r\n'
STOP = b'avc stp\r\n'
SWEEP = b'avc swp\r\n'
CENTER = b'avc ctr\r\n'
POTS = b'avc get pot\r\n'
ANGLE = b'avc get agl\r\n'
    
class AvcServo(object):
    arduino = None
    isRunning = False

    def __init__(self, target_port):
        self.arduino = serial.Serial(port = target_port, baudrate = 115200)
        time.sleep(3)
        return

    def receivePakcet(self):
        if self.arduino is None:
            logger.printErr("\/From startServo in AvcServo\/")
            logger.printErr("No Arduino detected")
            return []
        else:
            packet = self.arduino.readline()
            packet = str(packet.decode('ascii'))
            return packet.split('\r\n')

    def startServo(self):
        if self.arduino is None:
            logger.printErr("\/From startServo in AvcServo\/")
            logger.printErr("No Arduino detected")
        else:
            if self.isRunning:
                logger.printInfo("Servo already running!")
                return 0
            
            self.arduino.write(START)
            packet = self.receivePakcet()
            if packet[0] in ['ack']:
                self.isRunning = True
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From startServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1

    def stopServo(self):
        if self.arduino is None:
            logger.printErr("\/From stopServo in AvcServo\/")
            logger.printErr("No Arduino detected")
        else:
            self.arduino.write(STOP)
            packet = self.receivePakcet()
            if packet[0] in ['ack']:
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From stopServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1

    def sweepServo(self):
        if self.arduino is None:
            logger.printErr("\/From sweepServo in AvcServo\/")
            logger.printErr("No Arduino detected")
        else:
            if self.isRunning:
                logger.printInfo("Servo already running!")
                return 0
            
            self.arduino.write(SWEEP)
            packet = self.receivePakcet()
            if packet[0] in ['ack']:
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From sweepServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1
            
    def centerServo(self):
        if self.arduino is None:
            logger.printErr("\/From centerServo in AvcServo\/")
            logger.printErr("No Arduino detected")
        else:
            self.arduino.write(CENTER)
            packet = self.receivePakcet()
            if packet[0] in ['ack']:
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From centerServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1
