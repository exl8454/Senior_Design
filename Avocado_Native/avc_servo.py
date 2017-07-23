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

# Arduino control
START = b'avc_start\r\n'
STOP = b'avc stp\r\n'
SHUTDOWN = b'avc sdn\r\n'

# Streaming control
START_STREAM = b'avc srt str\r\n'
STOP_STREAM = b'avc stp str\r\n'

# Servo control
SWEEP = b'avc swp\r\n'
CENTER = b'avc ctr\r\n'

# Data control
GET_POTS = b'avc get pot\r\n'
GET_ANGLE = b'avc get agl\r\n'
GET_ANGLE_RAW = b'avc get agr\r\n'
GET_ALL = b'avc get\r\n'

# Calibration
CALIBRATE_A = b'avc clb tpa\r\n'
CALIBRATE_B = b'avc clb tpb\r\n'
CALIBRATE_C = b'avc clb tpc\r\n'
CALIBRATE_D = b'avc clb tpd\r\n'
SET_CENTER = b'avc set ctr\r\n'
    
class AvcServo(object):
    arduino = None
    isRunning = False

    pot_hi = 180
    pot_center = 90
    pot_lo = 0

    def __init__(self, target_port):
        self.arduino = serial.Serial(port = target_port, baudrate = 115200)

        packet = self.receivePacket()
        if packet[0] in ['ack']:
            return

    def isOpened(self):
        if self.arduino is None:
            logger.printErr("\/From Arduino Checking\/")
            logger.printErr("No Arduino detected")
            return False
        else:
            return True

    # General purpose data reading
    def receivePacket(self):
        if self.isOpened():
            packet = self.arduino.readline()
            packet = str(packet.decode('ascii'))
            packet = packet.split('\r\n')
            return packet[0].split(' ')
        else:
            return []

    # Use for data only!
    def readPacket(self):
        if self.isOpened():
            packet = self.arduino.readline()# Read in data
            packet = str(packet.decode('ascii'))
            packet = packet.split('\r\n') # Remove delimiter first
            packet = packet[0].split(' ') # Split data
            
            if len(packet) != 4:
                logger.printErr("\/From readPacket in AvcServo\/")
                logger.printErr("Incorrect packet size")
                return[]
            
            angle = int(packet[0])
            raw_angle = int(packet[1])
            pot_angle = float(packet[2])
            if packet[3] in ['ack']:
                return [angle, raw_angle, pot_angle]
            else:
                logger.printErr("\/From readPacket in AvcServo\/")
                logger.printErr("Improper ending code (No ACK)")
                return []
            
    # Opens port
    def openPort(self, target_port):
        if not self.isOpened():
            return
        
        if self.arduino.is_open:
            self.arduino.close()

        self.arduino = serial.Serial(port = target_port, baudrate = 115200)
        time.sleep(3)
        return

    # Closes port (Serves as shutdown sequence as well)
    def closePort(self):
        if not self.isOpened():
            return
        
        if not self.arduino.is_open:
            return

        self.arduino.write(SHUTDOWN)
        self.arduino.close()
        return

    # Sends start sequence (Not to be used as start sweep)
    def startServo(self):
        global pot_hi, pot_center, pot_lo
        if self.isOpened():
            if self.isRunning:
                logger.printInfo("Servo already running!")
                return 0
            
            self.arduino.write(START)
            packet = self.receivePacket()
            if packet[0] in ['ack']:
                self.isRunning = True
                return 0
            elif packet[0] in ['err']:
                if packet[1] in ['000']:
                    logger.printErr("\/From startServo in AvcServo\/")
                    logger.printErr("Servo angle mismatch")
                    return -1
                else:
                    logger.printErr("\/From startServo in AvcServo\/")
                    logger.printErr("Error Code " + packet[1])
                    return -1
            elif len(packet) == 0:
                logger.printErr("\/From startServo in AvcServo\/")
                logger.printErr("No packet received")
                return -1
        else:
            return -1

    # Sends start streaming signal (Do not use for actual data acquisition. Debug only)
    def startStreaming(self):
        if self.isOpened():
            self.arduino.write(START_STREAM)

    # Sends stop streaming signal (Do not use for actual data acquisition. Debug only)
    def stopStreaming(self):
        if self.isOpened():
            self.arduino.write(STOP_STREAM)
            packet = self.receivePacket()
            if packet[0] in ['ack']:
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From stopServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1
    
    # Sends stop signal (Does not terminate port)
    def stopServo(self):
        if self.isOpened():
            self.arduino.write(STOP)
            packet = self.receivePacket()
            if packet[0] in ['ack']:
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From stopServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1
        else:
            return -1

    # Moves servo to center
    def centerServo(self):
        if self.isOpened():
            self.arduino.write(CENTER)
            packet = self.receivePacket()
            if packet[0] in ['ack']:
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From centerServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1

    # Starts sweeping
    def sweepServo(self):
        if self.isOpened():
            self.arduino.write(SWEEP)
            packet = self.receivePacket()
            if packet[0] in ['ack']:
                return 0
            elif len(packet) == 0:
                logger.printErr("\/From sweepServo in AvcServo\/")
                logger.printErr("No packet received")
            else:
                return -1
        else:
            return -1

    # Sweeps to target angle
    def sweepTo(self, target):
        data = 'avc gto ' + str(target) + '\r\n'
        if self.isOpened():
            self.arduino.write(data.encode(encoding = 'ascii'))

            packet = self.receivePacket()
            if len(packet) != 2:
                logger.printErr("\/From sweepTo in AvcServo\/")
                logger.printErr("Packet size incorrect")
            else:
                logger.printInfo("Servo position set to " + packet[0])

    # Sends calibration
    def calibrateA(self):
        global pot_hi, pot_center, pot_lo
        if self.isOpened():
            self.arduino.write(CALIBRATE_A)
            packet = self.receivePacket()
            pot_hi = int(packet[0])
            pot_center = int(packet[1])
            pot_lo = int(packet[2])
            return (pot_hi, pot_center, pot_lo)

    def calibrateB(self):
        global pot_hi, pot_center, pot_lo
        if self.isOpened():
            self.arduino.write(CALIBRATE_B)
            packet = self.receivePacket()
            pot_hi = int(packet[0])
            pot_center = int(packet[1])
            pot_lo = int(packet[2])
            return (pot_hi, pot_center, pot_lo)

    def calibrateC(self):
        global pot_hi, pot_center, pot_lo
        if self.isOpened():
            self.arduino.write(CALIBRATE_C)
            packet = self.receivePacket()
            pot_hi = int(packet[0])
            pot_center = int(packet[1])
            pot_lo = int(packet[2])
            return (pot_hi, pot_center, pot_lo)

    def calibrateD(self):
        global pot_hi, pot_center, pot_lo
        if self.isOpened():
            self.arduino.write(CALIBRATE_D)

            packet = self.receivePacket()
            if packet[0] in ['rdy']:
                print("Servo is at lowest point. Adjust baseplate if needed.")
                input("Press Enter to Move to Next Position...")
                self.arduino.write(b'\r\n')

            packet = self.receivePacket()
            if packet[0] in ['rdy']:
                print("Servo is at center point. Adjust baseplate if needed.")
                input("Press Enter to Move to Next Position...")
                self.arduino.write(b'\r\n')

            packet = self.receivePacket()
            if packet[0] in ['rdy']:
                print("Servo is at highest point. Adjust baseplate if needed.")
                input("Press Enter to Move to Next Position...")
                self.arduino.write(b'\r\n')

            packet = self.receivePacket()
            pot_hi = int(packet[0])
            pot_center = int(packet[1])
            pot_lo = int(packet[2])
            return (pot_hi, pot_center, pot_lo)

    # Sends new delay interval for sweep
    def setDelay(self, _delay):
        data = 'avc set del ' + str(_delay) + '\r\n'
        if self.isOpened():
            self.arduino.write(data.encode(encoding = 'ascii'))

            packet = self.receivePacket()
            if len(packet) != 2:
                logger.printErr("\/From setDelay in AvcServo\/")
                logger.printErr("Packet size incorrect")
            else:
                logger.printInfo("Sweep interval set to " + packet[0])

    # Manually set potentiometer offset (Servo must be detached or is in center before doing so!)
    # Note that error signal will be sent if servo is in sweep motion
    def setCenter(self):
        global pot_center
        if self.isOpened():
            self.arduino.write(SET_CENTER)

            packet = self.receivePacket()
            if len(packet) != 2:
                logger.printErr("\/From setCenter in AvcServo\/")
                logger.printErr("Packet size incorrect")
            elif packet[0] in ['err']:
                if packet[1] in ['001']:
                    logger.printErr("\/From setCenter in AvcServo\/")
                    logger.printErr("Servo is in sweep motion. Stop servo first!")
                else:
                    logger.printErr("\/From setCenter in AvcServo\/")
                    logger.printErr("Error Code: " + packet[1])
            else:
                logger.printInfo("Potentiometer center set to " + packet[0])

    # Returns current servo angle
    def getAngle(self):
        if self.isOpened():
            self.arduino.write(GET_ANGLE)

            packet = self.receivePacket()
            if len(packet) != 2:
                logger.printErr("\/From getAngle in AvcServo\/")
                logger.printErr("Packet size incorrect")
            else:
                return int(packet[0])

    # Returns servo angle reading (Not the current servo angle!)
    def getAngleRaw(self):
        if self.isOpened():
            self.arduino.write(GET_ANGLE_RAW)

            packet = self.receivePacket()
            if len(packet) != 2:
                logger.printErr("\/From getAngleRaw in AvcServo\/")
                logger.printErr("Packet size incorrect")
            else:
                return int(packet[0])

    # Returns potentiometer reading
    def getPotentiometer(self):
        if self.isOpened():
            self.arduino.write(GET_POTS)

            packet = self.receivePacket()
            if len(packet) != 2:
                logger.printErr("\/From getPotentiometer in AvcServo\/")
                logger.printErr("Packet size incorrect")
            else:
                return float(packet[0])

    # Returns single reading
    def getSample(self):
        if self.isOpened():
            self.arduino.write(GET_ALL)
            return self.readPacket()
