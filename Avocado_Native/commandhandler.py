# commandhandler.py
# Handles commands

# Native Imports
import threading

# Third-party Imports

# Avocado Imports
from LidarHandler import LidarHandler as Lidar
import AvocadoLogger as logger
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
            cmd = command.split(" ")
            if cmd[0] in ['get']:
                pass # TODO Getter function
            elif cmd[0] in ['set']:
                # TODO setter function
               if cmd[1] in ['-m']: # Motor speed
                    if len(cmd) < 3 or len(cmd) > 3:
                        logger.printInfo("set -m usage")
                        logger.printInfo("set -m [pwm]")
                        pass
                    else:
                        if self.lidar is None:
                            logger.printErr("No LIDAR connected!")
                        else:
                            pwm = int(cmd[2])
                            if pwm > 1023:
                                pwm = 1023
                            elif pwm < 0:
                                pwm = 0
                            lidar.setSpeed(pwm)
                        
                        
            
            if command in ['start viz']:
                pass # TODO add visualizer code
            if command in ['set speed']:
                pass # TODO 
