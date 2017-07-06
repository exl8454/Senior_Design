#!/bin/bash
cd ~/sd
chmod 666 /dev/ttyUSB0
source devel/setup.bash
roslaunch rplidar_ros rplidar.launch

