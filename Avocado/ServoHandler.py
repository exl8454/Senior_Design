# ServoHandler.py
# Handles servo on Arduino
# NOTE
# HAVE NOT YET IMPLEMENTED SINCE I HAVE NO SERVO TO TEST

# Native import
import threading

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
def StartServo(target_port, time_out):
    arduino = serial.Serial(target_port, 115200, timeout = time_out)
    arduino.write("avc_start\n")
    while not(arduino.in_waiting >= 4):
        pass
    code = arduino.read()
    code = str(code.decode('utf-8'))
    if (code in ['ack']):
        return 0
    else:
        return -1

# Sends new delay between servo turn.
# Funtion will attempt to receive new delay from arduino then return the value.
def SetServoSpeed(delay_in_milli):
    if not(arduino is None):
        arduino.write("avc del " + str(delay_in_milli) + "\n")
        while not(arduino.in_waiting >= 4):
            pass
        value = arduino.read()
        if(code in [str(delay_in_milli)]):
           return value
    else:
        stream.PrintTo("No arduino detected", "ERR")
        return -1

# Sends signal to Arduino to force stop servo
def StopServo():
    if not(arduino is None):
        arduino.write("avc stp\n")
        while not(arduino.in_waiting >= 3):
            pass
        code = arduino.read()
        code = str(code.decode('utf-8'))
        if (code in ['ack']):
            return 0
        else:
            return -1
    else:
        stream.PrintTo("No arduino detected", "ERR")
        return -1

# Requests servo's current angle then saves to a variable
def GetServoAngle():
    if not(arduino is None):
        arduino.write("avc get agl\n")
        while not(arduino.in_waiting >= 3):
            pass
        code = arduino.read()
        code = str(code.decode('utf-8'))
        global servo_angle = int(code)

# Variables
servo_angle = 0;
