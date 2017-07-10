# ROSCore.py
# Core for ROS Node init and scan

# Native imports
import os
import signal
import subprocess
import threading
import StreamHandler
from time import sleep
import time

# Custom imports
import LidarParser as parser

class CommProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while running:
            print ("Type 'exit' to stop process...")
            command = ""
            while (command != "exit"):
                command = input("AVOCADO>>>")

            stream.PrintTo("Suspending Avocado...", "INFO")
            roscore.TerminateCore()
            stream.PrintTo("Goodby!", "INFO")

class InitProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        stream.PrintTo("Starting ROS Service...", "INFO")
        try:
            initProcess = subprocess.Popen('./runpy-1.sh', bufsize = -1, stdout = subprocess.PIPE)
            running = True;
        except Exception as oe:
            StreamHandler.WriteErr("From ROSCore.py; StartCore() ")
            StreamHandler.WriteErr("\t" + str(oe.strerror))
            StreamHandler.PrintTo("Terminating process...")
            StreamHandler.WriteLog("Terminating process...")
            StreamHandler.CloseAll()
            running = False;

class ScanProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global scanProcess, running
        global endtime, starttime

        stream.PrintTo("Creating ROS Node...", "INFO")
        try:
            scanProcess = subprocess.Popen('./runpy-2.sh', bufsize = -1, stdout = subprocess.PIPE)
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

# Start Core
def StartCore():
    global initProc, scanProc, commProc, running

    if not(running):
        StreamHandler.PrintTo("Creating Node...")
        initProc.start()
        scanProc.start()
        commProc.start()
        initProc.join()
        scanProc.join()
        commProc.join()

# Terminate Core
def TerminateCore():
	global scanProcess, initProcess

	StreamHandler.PrintTo("Terminating ROS Service...")
	if not(scanProcess is None) or not(initProcess is None):
            os.kill(initProcess.pid, signal.SIGINT)
            os.kill(scanProcess.pid, signal.SIGINT)
            #os.killpg(os.getpgid(scanProc.pid), signal.SIGINT)
            running = False

# Get Data
def GetData(channel = 0, decimalPlaces = 6):
    global scanProcess
    if not(scanProcess is None):
        outputline = scanProcess.stdout.readline()
        parser.ParseData(outputline)
    else:
        StreamHandler.WriteErr("scanProcess is still None")
    
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
