# ServoHandler.py
# Handles servo on Arduino
# NOTE
# HAVE NOT YET IMPLEMENTED SINCE I HAVE NO SERVO TO TEST

# Native import
import threading
import time

# Thrid-party import
import serial

# Custom import
import StreamHandler as stream

arduino = None

class ArduProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init(self)

    def run(self):
        pass

# Attempts to start arduino on target port.
# If started, arduino should return start code.
# Otherwise, arduino will return -1
def StartServo(target_port):
    global arduino
    arduino = serial.Serial(port = target_port, baudrate = 115200)
    time.sleep(3)
    arduino.write(b'avc_start\r')
    while (arduino.in_waiting <= 4):
        pass
    code = arduino.readline()
    code = str(code.decode('ascii'))
    if (code in ['ack\r\n']):
        return 0
    else:
        return -1

# Sends signal to Arduino to move servo angle to center (90 degrees)
def StopServo():
    global arduino
    if not(arduino is None):
        arduino.write(b'avc stp\r')
        while (arduino.in_waiting <= 4):
            pass
        code = arduino.readline()
        code = str(code.decode('ascii'))
        if (code in ['ack\r\n']):
            return 0
        else:
            return -1
    else:
        stream.PrintTo("No arduino detected", "ERR")
        return -1

# Sends new delay between servo turn.
# Funtion will attempt to receive new delay from arduino then return the value.
def SetServoSpeed(delay_in_milli):
    global arduino
    if not(arduino is None):
        cmd = "avc del " + str(delay_in_milli) + "\r"
        arduino.write(cmd.encode(encoding = 'ascii'))
        while not(arduino.in_waiting >= 4):
            pass
        value = int(arduino.readline())
        if value == delay_in_milli:
           return value
    else:
        stream.PrintTo("No arduino detected", "ERR")
        return -1

# Requests servo's current angle then saves to a variable
def GetServoAngle():
    global arduino
    if not(arduino is None):
        arduino.write(b'avc get agl\r')
        while not(arduino.in_waiting >= 3):
            pass
        code = arduino.readline()
        code = str(code.decode('ascii'))
        global servo_angle
        servo_angle = int(code)

# Variables
servo_angle = 0;
