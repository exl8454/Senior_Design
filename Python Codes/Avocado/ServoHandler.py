# ServoHandler.py
# Handles servo on Arduino

# Native import
import threading

# Thrid-part import
import serial

# Custom import

arduino = None

class ArduProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init(self)

    def run(self):

# Sends new delay between servo turn.
# Funtion will attempt to receive new delay from arduino then return the value.
def SetServoSpeed(delay_in_milli):
    if not(arduino is None):
        arduino.write("avc del " + str(delay_in_milli))
        while not(arduino.in_waiting >=
    else:
        PrintTo("No arduino detected", "ERR")
    return new_delay_in_milli

# Attempts to start arduino on target port.
# If started, arduino should return start code.
# Otherwise, arduino will return -1
def StartServo(target_port):
    arduino = serial.Serial(target_port, 115200, timeout = 10)
    arduino.write("avc_start")
    while not(arduino.in_waiting >= 4):
        pass
    code = arduino.read(4)
    code = str(code.decode('utf-8'))
    if (code in ['strt']):
        return 0
    else: return -1
