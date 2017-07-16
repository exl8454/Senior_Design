'''
    Config.py
    Used to store all Avocado configuration settings
'''

import FileHandler as fh
import AvocadoLogger as logger
import StreamHandler as avc_file # Deprecated

def readConfig():
    openFile = None
    openFile = fh.openFile("config.avocado")
    if openFile is None:
        logger.printInfo("Avocado didn't detect its configuration file!")
        logger.printInfo("Auto-generating default configuration...")
        openFile = fh.openFile("config.avocado")
        openFile.write("avocado_dump_data=False\n")
        openFile.write("avocado_read_interval=10\n")
        openFile.write("avocado_lidar_scan_type=0\n")
        openFile.write("avocado_servo_interval=15\n")
        openFile.write("avocado_serial_timeout=5\n")
        openFile.write("avocado_dump_location=AVC_DATA\n");
        openFile.write("avocado_lidar_linux=/dev/ttyUSB0\n");
        openFile.write("avocado_lidar_windows=COM6\n");
        openFile.close()
        ReadConfig()
    else:
        global settings
        logger.printInfo("Config file loaded, changing settings...")
        line = openFile.read()
        line = line.split("\n")
        avocado_dump_data = line[0].split("=")[1] in ['True', 'False']
        avocado_read_interval = int(line[1].split("=")[1])
        avocado_lidar_scan_type = int(line[2].split("=")[1])
        avocado_servo_interval = int(line[3].split("=")[1])
        avocado_serial_timeout = int(line[4].split("=")[1])
        avocado_dump_location = str(line[5].split("=")[1])
        avocado_lidar_linux = str(line[6].split("=")[1])
        avocado_lidar_windows = str(line[7].split("=")[1])
        settings = [avocado_dump_data,
            avocado_read_interval,
            avocado_lidar_scan_type,
            avocado_servo_interval,
            avocado_serial_timeout,
            avocado_dump_location,
            avocado_lidar_linux,
            avocado_lidar_windows]
        openFile.close()

# Variables
settings = [] # To save configuration
