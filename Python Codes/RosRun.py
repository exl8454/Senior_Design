import subprocess

print subprocess.Popen(["rosrun", "rplidar_ros", "rplidarNodeClient"], bufsize = -1).stdout.read()
