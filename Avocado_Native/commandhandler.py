# commandhandler.py
# Handles commands

# Native Imports
import threading

# Third-party Imports

# Avocado Imports
from LidarHandler import LidarHandler as Lidar
import AvocadoVis

class CommandHandler(threading.Thread):
    lidar = None
    
    def __init__(self, lidar):
        threading.Thread.__init__(self)
        self.lidar = lidar
        return

    def run(self):
        print("Type exit to terminate Avocado...")
        command = input("AVOCADO>>>")
        while not(command in ['exit']):
            command = input("ACOVADO>>>")
            # Command filter
            if command in ['start viz']:
                pass # TODO add visualizer code
