#!/bin/bash
cd ~/sd
echo 'Red!23' | sudo -S chmod 666 /dev/ttyUSB0
echo 'Red!23' | sudo -S source devel/setup.bash
echo 'Red!23' | sudo -S roslaunch rplidar_ros rplidar.launch
