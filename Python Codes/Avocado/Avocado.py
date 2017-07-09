# Avocado.py
# Front end to handle LIDAR and potentiometer

import StreamHandler as stream
import ROSCore as roscore

avocado_config = []

stream.PrintTo("Avocado 1.0", "INFO")
stream.PrintTo("Loading configuration file...", "INFO")

avocado_config = stream.ReadConfig()
if(avocado_config == -1):
    avocado_config = stream.ReadConfig()

stream.PrintTo("Setting local data dump position", "INFO")
#stream.InitFiles("/home/edward/Desktop/LIDARDUMP")
stream.InitFiles("LIDARDUMP")

stream.PrintTo("Starting ROS Service...", "INFO")

roscore.StartCore()

print ("Type exit to stop process...")
command = input("AVOCADO>>>")
while(command != "exit"):
    command = input("AVOCADO>>>")

stream.PrintTo("Suspending Avocado...", "INFO")
#TODO Add shutdown procedure
stream.PrintTo("Goodbye!", "INFO")
