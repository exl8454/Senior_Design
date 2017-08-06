# avc_data.py
# Handles data files

# Native Imports
import os
import os.path
from datetime import datetime

class AvcData(object):
    directory = ""
    _file = None
    
    def __init__(self, directory, filecount, option = "w"):
        self.directory = directory + "/DATA_" + str(datetime.today().date()) + "_" + str(filecount) + ".csv"

        while os.path.isfile(self.directory):
            filecount += 1
            self.directory = directory + "/DATA_" + str(datetime.today().date()) + "_" + str(filecount) + ".csv"
        
        self._file = open(self.directory, option)

        self._file.write("Time, Lidar_Angle, Lidar_Distance, Lidar_Intensity, Pot_Angle\n")
        self._file.close()
        
        return

    def writeTo(self, args):
        if self._file.closed:
            self._file = open(self.directory, "a")
            pass

        self._file.write(str(datetime.now()) + ", ")

        self._file.write(str(args[0]) + ", ")
        self._file.write(str(args[1]) + ", ")
        self._file.write(str(args[2]) + ", ")
        self._file.write(str(args[3]))
        
        self._file.write("\n")
        self._file.close()
        return

    def close(self):
        if not self._file.closed:
            self._file.close()
            pass
        return
