#!/bin/bash
cd ~/sd
echo 'Red!23' | sudo -S source devel/setup.bash
echo 'Red!23' | sudo -S rosrun rplidar_ros rplidarNodeClient
