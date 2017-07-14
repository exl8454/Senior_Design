'''
    Config.py
    Used to store all Avocado configuration settings
'''

import StreamHandler as avc_file

def ReadConfig():
    openFile = None
    openFile = avc_file.OpenFile("config.avocado")
    if openFile is None:
        avc_file.PrintTo("Avocado didn't detect its configuration file!", "INF")
        avc_file.PrintTo("Auto-generating default configuration...", "INF")
        openFile = avc_file.CreateFile("config.avocado", "w")
        openFile.write("avocado_dump_data=False\n")
        openFile.write("avocado_read_interval=10\n")
        openFile.write("avocado_lidar_scan_type=0\n")
        openFile.write("avocado_servo_interval=15\n")
        openFile.write("avocado_serial_timeout=5\n")
        openFile.write("avocado_dump_location=AVC_DATA\n");
        openFile.close()
        ReadConfig()
    else:
        global avocado_config
        avc_file.PrintTo("Config file loaded, changing settings...", "INF")
        line = openFile.read()
        line = line.split("\n")
        avocado_dump_data = line[0].split("=")[1] in ['True', 'False']
        avocado_read_interval = int(line[1].split("=")[1])
        avocado_lidar_scan_type = int(line[2].split("=")[1])
        avocado_servo_interval = int(line[3].split("=")[1])
        avocado_serial_timeout = int(line[4].split("=")[1])
        avocado_dump_location = str(line[5].split("=")[1])
        avocado_config = [avocado_dump_data,
            avocado_read_interval,
            avocado_lidar_scan_type,
            avocado_servo_interval,
            avocado_serial_timeout,
            avocado_dump_location]
        openFile.close()

# Variables
avocado_config = [] # To save configuration
