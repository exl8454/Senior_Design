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

class AvcServo(object):
    START = b'avc_start\r'
    CENTER = b'avc stp\r'
    POTS = b'avc get pot\r'
    ANGLE = b'avc get agl\r'

    arduino = None

    def __init__(self, target_port):
        self.arduino = serial.Serial(port = target_port, baudrate = 115200)
        time.sleep(3)
        return

    def startServo(self):
        if self.arduino is None:
            logger.printErr("\/From startServo in AvcServo\/")
            logger.printErr("No Arduino detected")
        else:
            arduino.write(START)
            packet = self.arduino.readline()
            packet = str(code.edcode('ascii'))
            packet = packet.split('\r\n')[0]
            if packet in ['ack']:
                return 0
            else:
                return -1
