"""
Avocado Native Version
"""
# Avocado.py
# Front end to handle LIDAR and potentiometer

# Native imports
import os

# Third-party imports

# Custom imports
import StreamHandler as stream
import ROSCore as roscore
import Config as avc_config

avocado_config = [] # To save configuration
avocado_filedir = "LIDARDUMP" # Default file directory
# Located inside Avocado folder

# Print start-up to Python shell
stream.PrintTo("Avocado 1.0", "INFO")
stream.PrintTo("Loading configuration file...", "INFO")

# Loads configuration from file.
# If configuration file is not found, Avocado will create new one with default
# Settings
avc_config.ReadConfig()

# Dump folder is re-directed from here
avocado_filedir = avc_config.avocado_config[5]

# Starts linking native files(data and dump) with Python
# Same as config file, if saving directory doesn't exist, Avocado will make
# new one
stream.PrintTo("Setting local data dump position", "INFO")
stream.PrintTo("Avocado will automatically create directory if it doesn't exist...", "INFO")
if not os.path.exists(avocado_filedir):
	os.makedirs(avocado_filedir)

# Once the directory is created, file linking is started.
stream.InitFiles(avocado_filedir)

# Starts back-end scripts. Refer to ROSCore.py
roscore.StartCore()
