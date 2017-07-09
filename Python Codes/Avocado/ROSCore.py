# ROSCore.py
# Core for ROS Node init and scan

import subprocess
import threading
import StreamHandler
import LidarParser as parser
from time import sleep
import time

class ScanProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global scanProcess, running
        global endtime, starttime
        
        try:
            scanProcess = subprocess.Popen('./runpy-1.sh', bufsize = -1, stdout = subprocess.PIPE)
            running = True;
        except Exception as oe:
            StreamHandler.WriteErr("From ROSCore.py; StartCore() ")
            StreamHandler.WriteErr("\t" + str(oe.strerror))
            StreamHandler.PrintTo("Terminating process...")
            StreamHandler.WriteLog("Terminating process...")
            StreamHandler.CloseAll()
            running = False;
        
        while running:
            GetData()
            endtime = int(round(time.time() * 1000))
            if(endtime - starttime > interval):
                StreamHandler.Write(parser.GetData())
                starttime = endtime
        StreamHandler.PrintTo("Thread Stopped")
                
def StartCore():
    global scanProc
    global dataProc

    StreamHandler.PrintTo("Creating Node...")
    scanProc.start()
    scanProc.join()

def GetData(channel = 0, decimalPlaces = 6):
    global scanProcess
    if not(scanProcess is None):
        outputline = scanProcess.stdout.readline()
        parser.ParseData(outputline)
    else:
        StreamHandler.WriteErr("scanProcess is still None")
    
scanProcess = None
scanProc = ScanProcess()
running = False

# For data
endtime = 0
starttime = 0
interval = 10
