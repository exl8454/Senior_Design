# ROSCore.py
# Core for ROS Node init and scan

import subprocess
import threading
import StreamHandler
import LidarParser

class InitProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global initProcess
        initProcess = subprocess.Popen('./runpy-1.sh', stdout = subprocess.PIPE)
        for line in initProcess.stdout:
            StreamHandler.WriteLog(line)

class ScanProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global scanProcess
        while True:
            GetData()

def StartCore():
    global initProcess, scanProcess
    global initProc, scanProc
    scanProcess = subprocess.Popen('./runpy-2.sh', bufsize = -1, stdout = subprocess.PIPE)
    initProc.start()
    initProc.join()
    scanProc.start()
    scanProc.join()

def GetData(channel = 0, decimalPlaces = 6):
    outputline = scanProcess.stdout.readline()
    LidarParser.ParseData(outputline)
    
initProcess = None
scanProcess = None

iniProc = InitProcess()
scanProc = ScanProcess()
