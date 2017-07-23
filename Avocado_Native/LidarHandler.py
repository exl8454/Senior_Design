'''
    LidarHandler.py
    Handles RPLidar via native control
    Python 3.6.1
'''
# Native Import
import sys
import time
import codecs
import struct
import threading

# Third-Party Import
import serial

# Avocado Import
import AvocadoLogger as logger
import Config as config

# Header constant
SYNC_A = b'\xA5'
SYNC_B = b'\x5A'

# Request packet constant
INFO = b'\x50'
STAT = b'\x52'
RATE = b'\x59'

# Control constant
STOP = b'\x25'
REST = b'\x40'

# Scan control constant
SCAN = b'\x20'

# Speed control constant (A2 only)
MOTOR_MAX_PWM = 10
MOTOR_PWM = 10
SPWM = b'\xF0'

# Data return size
DESC_LEN = 7
INFO_LEN = 20
STAT_LEN = 3
SCAN_LEN = 5

# Data type
INFO_TYPE = 4
STAT_TYPE = 6
SCAN_TYPE = 129

# From Avocado config
AVOCADO_CONFIG = config.settings

# Hardwares
A1 = 0
A2 = 2
    
def b2i(byte):
    return byte if int(sys.version[0]) == 3 else ord(byte)

def processSample(raw):
    new_scan = None
    agnle = -1
    distance = -1
    new_scan = bool(b2i(raw[0]) & 0b1)
    _new_scan = bool((b2i(raw[0]) >> 1) & 0b1)
    quality = b2i(raw[0]) >> 2
    if new_scan == _new_scan:
        logger.printErr("From process")
        logger.printErr("New Scan Flag Mismatch")
        return [], 0
    check_bit = b2i(raw[1]) & 0b1
    if check_bit != 1:
        logger.printErr("From process")
        logger.printErr("Check bit not equal to 1")
        return [], 0
    angle = ((b2i(raw[1]) >> 1) + (b2i(raw[2]) << 7)) / 64.
    distance = (b2i(raw[3]) + (b2i(raw[4]) << 8)) / 4.
    data = [new_scan, quality, angle, distance]
    return [data, len(data)]

class LidarProcess(object):
    _port = None    # For serial object
    port = ''       # For port selection
    port_timeout = 5# For UART data xmit timeout
    port_opened = False
    motor_speed = 0
    motor_running = False
    hardware = -1
    baudrate = 115200

    def __init__(self, port, pwm, timeout = 1):
        self.port = port
        self.baudrate = 115200
        self.port_timeout = timeout
        
        self.motor_speed = pwm
        self.motor_running = False

        self.scanning = False

        self.openPort()
        time.sleep(1)
        info = self.readInfo()
        self.hardware = int(info['hardware'])
        self.startMotor()
    '''
        Returns target port
        Returns: Serial object of port
        Returns: None if target port is not set
    '''
    def get_port(self):
        return _port

    '''
        Returns target port name
        Returns: String for port name
    '''
    def getPort(self):
        return port

    def start(self):
        self.openPort()
        time.sleep(1)
        info = self.readInfo()
        self.hardware = int(info['hardware'])
        self.startMotor()

    '''
        Opens serial port with preset configurations.
        If target port is not set, it will send error
        Exception: Port is None or Port is not found
    '''
    def openPort(self):
        if self._port is not None:
            self._port.close()
            
        if self.port is None:
            logger.printErr("Target port is not set!")
            return -1
        try:
            self._port = serial.Serial(\
                self.port, self.baudrate,\
                parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,\
                timeout = self.port_timeout)
            self.port_opened = True
        except serial.SerialException as ser:
            logger.printErr("\/Encountered error while trying to open port\/")
            logger.printErr(ser)
            return -1

    '''
        Closes serial port
    '''
    def closePort(self):
        if self._port is not None:
            self._port.close()
            self._port = None
        return

    '''
        Sends single command. This is for none-requesting type
        commands.
    '''
    def sendCmd(self, cmd):
        _cmd = SYNC_A + cmd
        self._port.write(_cmd)
        return

    '''
        Sends single command with parameter.
    '''
    def sendCmdWithVal(self, cmd, value):
        size = struct.pack('B', len(value))
        pack = SYNC_A + cmd + size + value
        cs = 0 # checksum
        for v in struct.unpack('B' * len(pack), pack):
            cs ^= v
        pack += struct.pack('B', cs)
        self._port.write(pack)
        return

    '''
        (A2 Only) Changes motor speed via pwm value
    '''
    def setSpeed(self, pwm = MOTOR_PWM):
        if self.hardware == A2:
            self.motor_speed = pwm
            pack = struct.pack("<H", pwm)
            self.sendCmdWithVal(SPWM, pack)
        elif self.hardware == A1:
            logger.printErr("A1 cannot set PWM!")
        return

    '''
        Starts Motor
    '''
    def startMotor(self):
        self._port.setDTR(False)
        if self.hardware == A2:
            self.setSpeed(self.motor_speed)
        self.motor_running = True
        return

    '''
        Stops motor. You can use setSpeed(0) as well to stop motor,
        but if DTR is LOW, it may cause trouble.
    '''
    def stopMotor(self):
        self._port.setDTR(True)
        if self.hardware == A2:
            self.setSpeed(0)
        time.sleep(0.005)
        self.motor_running = False
        return

    '''
        Reads header of response
    '''
    def readDesc(self):
        desc = self._port.read(DESC_LEN)
        if len(desc) != DESC_LEN:
            logger.printErr("From readDesc")
            logger.printErr("Discriptor length mismatch")
        elif not desc.startswith(SYNC_A + SYNC_B):
            logger.printErr("From readDesc")
            logger.printErr("Incorrect starting bytes")
            return 0
        is_single = b2i(desc[-2]) == 0
        return [b2i(desc[2]), is_single, b2i(desc[-1])]

    '''
        Reads actual response from LIDAR
    '''
    def readResp(self, pack_size):
        while self._port.inWaiting() < pack_size:
            time.sleep(0.001)
        data = self._port.read(pack_size)
        if len(data) != pack_size:
            logger.printErr("From readResp()")
            logger.printErr("Byte size does not match")
        return data

    '''
        Reads information from LIDAR
        Information contains
        Model, Firmware, Hardware, and Serial number.
    '''
    def readInfo(self):
        self.clearBuffer()
        if self._port.inWaiting() > 0:
            logger.printErr("From readInfo")
            logger.printErr("Buffer is not empty. Try flushing out buffer first")
            return -1
            
        self.sendCmd(INFO)
        desc = self.readDesc()
        if desc[0] != INFO_LEN:
            logger.printErr("From readInfo")
            logger.printErr("Info length mismatch")
            return -1
        if not desc[1]:
            logger.printErr("From readInfo")
            logger.printErr("Response is not a single (Its multiple)")
            return -1
        if desc[2] != INFO_TYPE:
            logger.printErr("From readInfo")
            logger.PrinTo("Response expected as info, received " + str(desc[2]) + " instead")
            return -1

        raw = self.readResp(desc[0])
        serial = codecs.encode(raw[4:], 'hex').upper()
        serial = codecs.decode(serial, 'ascii')
        data = {
            'model' : b2i(raw[0]),
            'firmware' : (b2i(raw[2]), b2i(raw[1])),
            'hardware' : b2i(raw[3]),
            'serial' : serial
            }
        return data

    '''
        Reads connected device's status
    '''
    def readStat(self):
        self.clearBuffer()
        if self._port.inWaiting() > 0:
            logger.printErr("From readStat")
            logger.printErr("Buffer is not empty. Try flushing out buffer first")
            return -1
            
        self.sendCmd(STAT)
        desc = self.readDesc()
        if desc[0] != STAT_LEN:
            logger.printErr("From readStat")
            logger.printErr("Stat length mismatch")
            return -1
        if not desc[1]:
            logger.printErr("From readStat")
            logger.printErr("Response is not a single (Its multiple)")
            return -1
        if desc[2] != STAT_TYPE:
            logger.printErr("From readStat")
            logger.PrinTo("Response expected as info, received " + str(desc[2]) + " instead")
            return -1
        raw = self.readResp(desc[0])
        stat = b2i(raw[0])
        err = (b2i(raw[1]) << 8) + b2i(raw[2])
        return [stat, err]

    '''
        Clears data buffer
    '''
    def clearBuffer(self):
        if self.scanning:
            logger.printErr("From clearBuffer")
            logger.printErr("Buffer cannot be cleared: Still scanning")
            return 0
        self._port.flushInput()
        return 1

    # Force clears buffer
    # Do not use unless you know what you are doing
    def f_clearBuffer(self):
        self._port.flushInput()
        while self._port.in_waiting:
            self._port.read()
        return

    '''
        Stops scanning
    '''
    def stopScan(self):
        self.sendCmd(STOP)
        time.sleep(.003)
        self.scanning = False
        self.clearBuffer()
        self.f_clearBuffer()

    '''
        Starts normal scan
    '''
    def startScan(self):
        if self.scanning:
            logger.printErr("From startScan()")
            logger.printErr("Already scanning")
            return -1
        stat = self.readStat()
        if stat[0] == 2:
            logger.printErr("From startScan()")
            logger.printErr("Error in sensor. Resetting...")
            self.reset()
            stat = self.readStat()
            if stat[0] == 2:
                logger.printErr("From startScan()")
                logger.printErr("Cannot reset LIDAR; hardware fault?")
                return -1
        elif stat[0] == 1:
            logger.printErr("From startScan()")
            logger.printErr("Scanning with LIDAR Warning")
            
        self.sendCmd(SCAN)
        
        desc = self.readDesc()
        if desc[0] != SCAN_LEN:
            logger.printErr("From startScan()")
            logger.printErr("Scan size mismatch")
            return -1
        if desc[1]:
            logger.printErr("From startScan()")
            logger.printErr("Head returned single response")
            return -1
        if desc[2] != SCAN_TYPE:
            logger.printErr("From startScan()")
            logger.printErr("Not a proper scan tytpe")
            return -1
        self.scanning = True
        return

    '''
        Resets device
        Do not use too often.
    '''
    def reset(self):
        self.sendCmd(REST)
        time.sleep(1)
        self.clearBuffer()
        return

    '''
        Returns single sample from LIDAR
        if leaveHigh parameter is set to True,
        LIDAR will remain in scan mode.
    '''
    def getSample(self, leaveHigh = True):
        if not self.motor_running:
            self.startMotor()
        if not self.scanning:
            self.startScan()

        raw = self.readResp(SCAN_LEN)
        data = processSample(raw)[0]
        while data[2] == 0.0: # This will dump invalid data
            raw = self.readResp(SCAN_LEN)
            data = processSample(raw)[0]

        sample = processSample(raw)[0]

        if not leaveHigh:
            self.stopScan()

        return sample

    def getScan(self):
        if not self.motor_running:
            self.startMotor()
        if not self.scanning:
            self.startScan()
            
        scan = []

        startNode = self.getSample(True)
        while startNode[1] == 0.0:
            startNode = self.getSample(True)
            
        while not startNode[0]:
            startNode = self.getSample(True)
        scan.insert(0, startNode)
        node = self.getSample(True)
        while not node[0]:
            scan.append(node)
            node = self.getSample(True)

        self.stopScan()

        return scan

# Lidar handler will start with single sampling to get warm up
class LidarHandler(object):
    lidar = None
    last_sample = None
    last_scan = []

    continuous = False
    
    def __init__(self, port, pwm):
        self.lidar = LidarProcess(port, pwm)
        last_sample = self.lidar.getSample(False)
        return

    # Function will return full 360 scan
    def getFullScan(self):
        if self.lidar is None:
            logger.printErr("\/From getFullScan() in class LidarHandler\/")
            logger.printErr("Lidar is not initialized!")
        else:
            self.last_scan = self.lidar.getScan()
            
            return self.last_scan

    # Function will return single sample
    def getNode(self, leaveHigh):
        if self.lidar is None:
            logger.printErr("\/From getNode() in class LidarHandler\/")
            logger.printErr("Lidar is not initialized!")
        else:
            self.last_sample = self.lidar.getSample(leaveHigh)

            return self.last_sample

    def stop(self):
        if self.lidar is None:
            logger.printErr("\/From stop() in class LidarHandler\/")
            logger.printErr("Lidar is not initialized!")
        else:
            self.lidar.stopScan()
            self.lidar.reset()
            self.lidar.stopMotor()
            return

    def start(self):
        if self.lidar is None:
            logger.printErr("\/From start() in class LidarHandler\/")
            logger.printErr("Lidar is not initialized!")
        else:
            self.last_scan = self.lidar.getScan(False)
            return

    def open(self):
        if self.lidar is None:
            logger.printErr("\/From open() in class LidarHandler\/")
            logger.printErr("Lidar is not initialized!")
        else:
            self.lidar.openPort()
            
    def close(self):
        if self.lidar is None:
            logger.printErr("\/From close() in class LidarHandler\/")
            logger.printErr("Lidar is not initialized!")
        else:
            self.lidar.closePort()
