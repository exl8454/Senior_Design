import sys, os
import subprocess

# Directly opens input and output stream using PIPE object
# bufsize = -1 allocates maximum buffer memory for this pipeline
rtncode = subprocess.Popen(['pwd'], shell = True, stdout = subprocess.PIPE)
for line in rtncode.stdout:
    print (line)
rtncode = subprocess.Popen(['ls', '-a'], shell = True, stdout = subprocess.PIPE)
for line in rtncode.stdout:
    print (line)
rtncode = subprocess.Popen(['./runpy-1.sh'], stdout = subprocess.PIPE)
while(True):
    print (rtncode.stdout.readline())
    
print ("End of bash run")

#rtncode = subprocess.check_output('./pyrun.sh', shell = True)
#print (rtncode)
#os.chmod('/dev/ttyUSB0', 666);
#rtncode = subprocess.run(['sudo', 'chmod', '666', '/dev/ttyUSB0'], shell = True)
#print ("Return Code: ", rtncode.returncode)
#os.system('source devel/setup.bash')
#rtncode = subprocess.check_output(['sudo', 'source', 'devel/setup.bash'], shell = True)
#print ("Return Code: ", rtncode.returncode)
#os.system('roslaunch rplidar_ros rplidar.launch')
#rtncode = subprocess.check_output(['sudo', 'roslaunch', 'rplidar_ros', 'rplidar.launch'], shell = True)
#print ("Return Code: ", rtncode.returncode)

#print ("Return Code: ", rtncode.returncode)

#while(1):
#pipe = subprocess.Popen('./runpy.sh', bufsize = -1, stdout = subprocess.PIPE, shell = True)
#pipe = subprocess.Popen(['rosrun', 'rplidar_ros', 'rplidarNodeClient', '>', 'dump.txt'], bufsize = -1, stdout = subprocess.PIPE, shell = True)
#print  ("Decoded: ", pipe)
