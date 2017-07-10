# Avocado.py
# Front end to handle LIDAR and potentiometer

# Native imports
import os
import _thread

# Third-party imports

# Custom imports
import StreamHandler as stream
import ROSCore as roscore

avocado_config = []
avocado_filedir = "LIDARDUMP"
#avocado_filedir = "/home/edward/Desktop/LIDARDUMP"

stream.PrintTo("Avocado 1.0", "INFO")
stream.PrintTo("Loading configuration file...", "INFO")

avocado_config = stream.ReadConfig()
if(avocado_config == -1):
    avocado_config = stream.ReadConfig()

stream.PrintTo("Setting local data dump position", "INFO")
stream.PrintTo("Avocado will automatically create directory if it doesn't exist...", "INFO")
if not os.path.exists(avocado_filedir):
	os.makedirs(avocado_filedir)

stream.InitFiles(avocado_filedir)

stream.PrintTo("Starting ROS Service...", "INFO")

thread.start_new_thread(CommandControl(), ())
roscore.StartCore()

def CommandControl():
    print ("Type exit to stop process...")
    command = ""
    while (command != "exit"):
        command = input("AVOCADO>>>")

    stream.PrintTo("Suspending Avocado...", "INFO")
    roscore.TerminateCore()
    stream.PrintTo("Goodby!", "INFO")
