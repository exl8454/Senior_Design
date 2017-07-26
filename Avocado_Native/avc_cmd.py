# avc_cmd.py
# Command Handler

# Native Imports

# Third-Party Imports

# Avocado Imports
from LidarHandler import LidarHandler as Lidar
import AvocadoLogger as logger
import AvocadoVis

class CommandHandler(object):
    lidar = None # LIDAR Ojbect
    vis = None # Visualizer
    servo = None # Arduino

    def __init__(self, lidar, vis, servo):
        self.lidar = lidar
        if self.lidar is None:
            logger.printErr("LIDAR Object is not defined")
        self.vis = vis
        if self.vis is None:
            logger.printErr("Avocado Visualizer is not defined")
        self.servo = servo;
        if self.servo is None:
            logger.printErr("Servo hanlder is not defined")
        return

    def run(self):
        command = ""
        
        print("Type exit to terminate Avocado...")
        while not(command in ['exit']):
            command = input("AVOCADO>>>")

            cmd = command.split(" ")
            if cmd[0] in ['get']: # Getter Functions
                pass
             elif cmd[0] in ['set']: # Setter Functions
                if cmd[1] in ['-lm']: # LIDAR Motor speed
                    if len(cmd) > 3:
                        logger.printInfo("set -lm usage")
                        logger.printInfo("set -lm [pwm]")
                        logger.printInfo("set -lm without thrid param will set motor speed to default")
                        pass
                    else:
                        if not(self.lidar is None):
                            if len(cmd) == 2: # Set to default speed
                                self.lidar.setSpeedDefault()
                                pass
                            elif len(cmd) == 3:
                                pwm = int(cmd[2])
                                if pwm > 1023:
                                    pwm = 1023
                                elif pwm < 0:
                                    pwm = 0

                                self.lidar.setSpeed(pwm)
                                pass
                            pass
                        pass
                    pass
                pass
            elif cmd[0] in ['startgfx']:
                if not(self.vis is None):
                    self.vis.startgfx();
                
                        
            
