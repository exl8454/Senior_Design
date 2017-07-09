# Avocado.py
# Front end to handle LIDAR and potentiometer

import StreamHandler as stream
import ROSCore

stream.PrintTo("Avocado 1.0", "INFO")
stream.PrintTo("Setting local data dump position", "INFO")
stream.InitFiles("/home/edward/Desktop/LIDARDUMP")

stream.PrintTo("Starting ROS Service...", "INFO")

ROSCore.StartCore()
