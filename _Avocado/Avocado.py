"""
Avocado Native Version
"""
# Avocado.py
# Front end to handle LIDAR and potentiometer

# Native imports
import os
import os.path
import platform

# Third-party imports

# Custom imports
import FileHandler as filehandler
import AvocadoLogger as logger
from AvocadoLogger import Avocado_Logger as Output
import StreamHandler as stream
import ROSCore as roscore
import Config as config
from datetime import datetime

# Print start-up to Python shell
logger.printInfo("Avocado 1.0")
logger.printInfo("Loading configuration file...")

filecount = 0
# Config first
config.readConfig()

# Folder check (Checks if folder exsists)
if not (os.path.isdir(config.settings[5])):
        os.mkdir(config.settings[5])

# Load default dump location
avocado_filedir = config.settings[5]
dataDumpLocation = config.settings[5] + "/DATA_" + str(filecount) + "_" + str(datetime.today().date()) + ".csv"
logDumpLocation = config.settings[5] + "/DUMP_" + str(filecount) + "_" + str(datetime.today().date()) + ".txt"

while os.path.isfile(dataDumpLocation):
        filecount += 1
        dataDumpLocation = config.settings[5] + "/DATA_" + str(filecount)  + "_" + \
                           str(datetime.today().date()) +  ".csv"
        logDumpLocation = config.settings[5] + "/DUMP_" + str(filecount)  + "_" + \
                          str(datetime.today().date()) +  ".txt"

while os.path.isfile(logDumpLocation):
        filecount += 1
        dataDumpLocation = config.settings[5] + "/DATA_" + str(filecount)  + "_" + \
                           str(datetime.today().date()) +  ".csv"
        logDumpLocation = config.settings[5] + "/DUMP_" + str(filecount)  + "_" + \
                          str(datetime.today().date()) +  ".txt"

logger.printInfo("Data dump location set to\/")
logger.printInfo(dataDumpLocation)
logger.printInfo("Dump location set to\/")
logger.printInfo(logDumpLocation)

# Load file objects
dataOut = Output(dataDumpLocation)
dumpOut = Output(logDumpLocation)

# Check system and set port location
portLocation = ""
if platform.system() in ['windows', 'Windows', 'WINDOWS']:
        portLocation = config.settings[7]
elif platform.system() in ['linux', 'Linux', 'LINUX']:
        portLocation = config.settings[6]

logger.printInfo("LIDAR port is set to " + portLocation)

# TODO Add start sequence
# Link Lidar first

'''
# Starts back-end scripts. Refer to ROSCore.py
roscore.StartCore()
'''
