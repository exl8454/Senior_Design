# Avocado.py
# Front end to handle LIDAR and potentiometer

import StreamHandler
import ROSCore

# Write
StreamHandler.InitFiles("LIDARDUMP")

ROSCore.StartCore()
