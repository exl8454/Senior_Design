# ROSPy.py
# Initiates ROS, then starts LIDAR
# Python 3.x

import os
import os.path
import subprocess
import spidev
import time
from time import sleep
from datetime import datetime
import threading

import RPLidar

# InitProc thread will initialize RPLidar to use
initProc = InitProcess()

# ScanProc thread will handle data from potentiometer and LIDAR
scanProc = ScanProcess()

dumpFile # Used to dump EVERYTHING
dataFile # Used to save all proper data



# Start initProc first
initProc.start()
initProc.join()
scanProc.start()
scanProc.join()
