# ROSCore.py
# Core for ROS Node init and scan

# Native imports
import os
import signal
import subprocess
import threading
import StreamHandler as stream
from time import sleep
import time

# Custom imports
import LidarParser as parser

class InitProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        stream.PrintTo("Starting ROS Service...", "INFO")
        try:
            initProcess = subprocess.Popen('./runpy-1.sh')
        except Exception as oe:
            stream.WriteErr("From ROSCore.py; StartCore() ")
            stream.WriteErr("\t" + str(oe.strerror))
            stream.PrintTo("Terminating process...")
            stream.WriteLog("Terminating process...")
            stream.CloseAll()
            running = False;

class ScanProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global scanProcess, running
        global endtime, starttime

        stream.PrintTo("Creating ROS Node...", "INFO")
        try:
            scanProcess = subprocess.Popen('./runpy-2.sh', bufsize = 1, stdout = subprocess.PIPE)
            running = True;
        except Exception as oe:
            stream.WriteErr("From ROSCore.py; StartCore() ")
            stream.WriteErr("\t" + str(oe.strerror))
            stream.PrintTo("Terminating process...")
            stream.WriteLog("Terminating process...")
            stream.CloseAll()
            running = False;
        
        while running:
            GetData()
            endtime = int(round(time.time() * 1000))
            if(endtime - starttime > interval):
                stream.Write(parser.GetData())
                starttime = endtime
        stream.PrintTo("Thread Stopped")

class CommProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print ("Type 'exit' to stop process...")
        command = ""
        while (command != "exit"):
            command = input("AVOCADO>>>")

        stream.PrintTo("Suspending Avocado...", "INFO")
        TerminateCore()
        stream.PrintTo("Goodby!", "INFO")

# Start Core
def StartCore():
    global initProc, scanProc, commProc, running

    if not(running):
        stream.PrintTo("Creating Node...", "INFO")
        initProc.start()
        scanProc.start()
        commProc.start()
        initProc.join()

# Terminate Core
def TerminateCore():
    global scanProcess, initProcess

    running = False
    
    stream.PrintTo("Terminating ROS Service...")
    if not(scanProcess is None):
        os.killpg(os.getpgid(scanProcess.pid), signal.SIGTERM)
    #if not(initProcess is None):
        #os.killpg(os.getpgid(initProcess.pid), signla.SIGTERM)

# Get Data
def GetData(channel = 0, decimalPlaces = 6):
    global scanProcess
    if not(scanProcess is None):
        outputline = scanProcess.stdout.readline()
        parser.ParseData(outputline)
    else:
        stream.WriteErr("scanProcess is still None")
    
scanProcess = None
initProcess = None
scanProc = ScanProcess()
initProc = InitProcess()
commProc = CommProcess()
running = False

# For data
endtime = 0
starttime = 0
interval = 10
