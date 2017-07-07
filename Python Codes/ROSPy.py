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

from RPLidar import *
