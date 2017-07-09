#!/bin/bash
cd ~/sd
ls /dev/ttyUSB0
echo -e "Red!23\n" | sudo -S chmod 666 /dev/ttyUSB0
source devel/setup.bash
roslaunch rplidar_ros rplidar.launch & rosrun rplidar_ros rplidarNodeClient
