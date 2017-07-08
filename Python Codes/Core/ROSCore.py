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

        try:
            initProcess = subprocess.Popen('./runpy-1.sh', stdout = subprocess.PIPE)
            running = True;
        except OSError as oe:
            StreamHandler.WriteErr("From ROSCore.py; InitProcess() ")
            StreamHandler.WriteErr("\t" + str(oe.strerror))
            StreamHandler.PrintTo("Terminating process...")
            StreamHandler.WriteLog("Terminating process...")
            StreamHandler.CloseAll()
            running = False;

        if not(initProcess is None):    
            for line in initProcess.stdout:
                StreamHandler.WriteLog(line)

class ScanProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global scanProcess, running
        while running:
            GetData()

def StartCore():
    global initProcess, scanProcess
    global initProc, scanProc
    global running
    
    try:
        scanProcess = subprocess.Popen('./runpy-2.sh', bufsize = -1, stdout = subprocess.PIPE)
        running = True;
    except OSError as oe:
        StreamHandler.WriteErr("From ROSCore.py; StartCore() ")
        StreamHandler.WriteErr("\t" + str(oe.strerror))
        StreamHandler.PrintTo("Terminating process...")
        StreamHandler.WriteLog("Terminating process...")
        StreamHandler.CloseAll()
        running = False;
        
    initProc.start()
    initProc.join()
    scanProc.start()
    scanProc.join()

def GetData(channel = 0, decimalPlaces = 6):
    global scanProcess
    if not(scanProcess is None):
        outputline = scanProcess.stdout.readline()
        LidarParser.ParseData(outputline)
    
initProcess = None
scanProcess = None

initProc = InitProcess()
scanProc = ScanProcess()

running = False
