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
import StreamHandler as logger
import Config as avc_config

# Header constant
SYNC_A = b'\xA5'
SYNC_B = b'\x5A'

# Request packet constant
INFO = b'\x50'
STAT = b'\x52'
RATE = b'\x59'
REST = b'\x40'

# Control constant
START = b'\x25'
STOP = b'\x40'

# Scan control constant
SCAN = b'\x20'

# Speed control constant (A2 only)
MOTOR_MAX_PWM = 1023
MOTOR_PWM = 660
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
AVOCADO_CONFIG = avc_config.avocado_config
    
def b2i(byte):
    return byte if int(sys.version[0]) == 3 else ord(byte)

def process(raw):
    new_scan = bool(b2i(raw[0]) & 0b1)
    _new_scan = bool((b2i(raw[0]) >> 1) & 0b1)
    quality = b2i(raw[0]) >> 2
    if new_scan == _new_scan:
        logger.PrintTo("New Scan Flag Mismatch", "ERR")
    check_bit = b2i(raw[0]) >> 2
    if check_bit != 1:
        logger.PrintTo("Check bit not equal to 1", "ERR")
    angle = ((b2i(raw[1]) >> 1) + (b2i(raw[2]) << 7)) / 64.
    distance = (b2i(raw[3]) + (b2i(raw[4]) << 8)) / 4.
    return [new_scan, quality, angle, distance]

class LidarProcess(object):
    _port = None    # For serial object
    port = ''       # For port selection
    port_timeout = 5# For UART data xmit timeout

    def __init__(self, port, timeout = 5):
        self.port = port
        self.baudrate = 115200
        self.timeout = timeout
        
        self.motor_speed = MOTOR_PWM
        self.motor_running = None

        self.scanning = False
        
    '''
        Returns target port
        Returns: Serial object of port
        Returns: None if target port is not set
    '''
    def get_port():
        return _port

    '''
        Returns target port name
        Returns: String for port name
    '''
    def getPort():
        return port

    '''
        Opens serial port with preset configurations.
        If target port is not set, it will send error
        Exception: Port is None or Port is not found
    '''
    def open():
        if self._port is not None:
            self.close()
        elif self.port is None:
            logger.WriteErr("Target port is not set!")
        try:
            self._port = serial.Serial(
                self.port, 115200,
                parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,
                timeout = self.port_timeout, dsrdtr = True)
        except serial.SerialException as ser:
            logger.WriteErr("\/Encountered error while trying to open port\/")
            logger.WriteErr(err)

    '''
        Closes serial port
    '''
    def close():
        if self._port is not None:
            self._port.close()

        return

    def sendCmd(self, cmd):
        _cmd = SYNC_A + cmd
        self._port.write(_cmd)
        return

    def sendCmd(self, cmd, value):
        size = struct.pack('B', len(value))
        pack = SYNC_BYTE + cmd + size + payload
        cs = 0 # checksum
        for v in struct.unpack('B' * len(pack), pack):
            cs ^= v
        pack += struct.pack('B', cs)
        self._port.write(pack)
        return

    def setSpeed(self, pwm = MOTOR_PWM):
        self.motor_speed = pwm
        if self.motor_running:
            pack = struct.pack("<H", self.motor_speed)
            self.sendCmd(SPWM, pack)
        return

    def startMotor(self):
        self._port.setDTR(False)
        self.setSpeed(self.motor_speed)
        self.motor_running = True
        return

    def stopMotor(self):
        self.setSpeed(0)
        time.sleep(0.005)

        self._port.setDTR(True)
        self.motor_running = False

    def readDesc(self):
        desc = self._port.read(DESC_LEN)
        if len(desc) != DESC_LEN:
            logger.PrintTo("Discriptor length mismatch", "ERR")
        elif not desc.startswith(SYNCA + SYNCB):
            logger.PrintTo("Incorrect starting bytes", "ERR")
        is_single = b2i(desc[-2]) == 0
        return [b2i(desc[2]), is_single, b2i(desc[-1])]

    def readResp(self, pack_size):
        while self._port.inWaiting() < pack_size:
            time.sleep(0.001)
        data = self._port.read(pack_size)
        return data

    def readInfo(self):
        if self._port.inWaiting() > 0:
            logger.PrintTo("Buffer is not empty. Try flushing out buffer first", "ERR")
            return -1
        self.sendCmd(INFO)
        desc = self.readDesc()
        if desc[0] != INFO_LEN:
            logger.PrintTo("Info length mismatch", "ERR")
            return -1
        if not desc[1]:
            logger.PrintTo("Response is not a single (Its multiple)", "ERR")
            return -1
        if desc[2] != INFO_TYPE:
            logger.PrinTo("Response expected as info, received " + str(desc[2]) + " instead", "ERR")
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

    def readStat(self):
        if self._port.inWaiting() > 0:
            logger.PrintTo("Buffer is not empty. Try flushing out buffer first", "ERR")
            return -1
        self.sendCmd(STAT)
        desc = self.readDesc()
        if desc[0] != STAT_LEN:
            logger.PrintTo("Info length mismatch", "ERR")
            return -1
        if not desc[1]:
            logger.PrintTo("Response is not a single (Its multiple)", "ERR")
            return -1
        if desc[2] != STAT_TYPE:
            logger.PrinTo("Response expected as info, received " + str(desc[2]) + " instead", "ERR")
            return -1
        raw = self.readResp(desc[0])
        stat = b2i(raw[0])
        err = (b2i(raw[1]) << 8) + b2i(raw[2])
        return [stat, err]

    def clearBuffer(self):
        if self.scanning:
            logger.PrintTo("Buffer cannot be cleared: Still scanning", "ERR")
            return -1
        self._port.flushInput()

    def stopScan(self):
        self.sendCmd(STOP)
        time.sleep(.2)
        self.scanning = False
        self.clearBuffer()

    '''
        Starts normal scan
    '''
    def startScan(self):
        if self.scanning:
            logger.PrintTo("Already scanning", "ERR")
            return -1
        stat = self.readStat()
        if stat[0] == 2:
            logger.PrintTo("Error in sensor. Resetting...", "ERR")
            self.reset()
            stat = self.readStat()
            if stat[0] == 2:
                logger.PrintTo("Cannot reset LIDAR; hardware fault?", "ERR")
                return -1
        elif stat[0] == 1:
            logger.PrintTo("Scanning with LIDAR Warning", "INF")
            
        self.sendCmd(SCAN)
        desc = self.readDesc()
        if desc[0] != SCAN_LEN:
            logger.PrintTo("Scan size mismatch", "ERR")
            return -1
        if desc[1]:
            logger.PrintTo("Head returned single response", "ERR")
            return -1
        if desc[2] != SCAN_TYPE:
            logger.PrintTo("Not a proper scan tytpe", "ERR")
            return -1
        self.scanning = True
        return

    def reset(self):
        self.sendCmd(REST)

class LidarHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
