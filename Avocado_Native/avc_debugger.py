# avc_debugger.py
# Debugging script (Scratch)

from avc_servo import AvcServo as AS
from avc_file import AvcFile as AF
from avc_logger import AvcLogger as AL
from avc_data import AvcData as AD
import avc_lidar
from avc_servo import AvcServo as Servo
from avc_vis import AvcVis as AV

from subprocess import Popen, PIPE

lidarProcess = Popen(['python3', 'avc_lidar'], stdin=PIPE, stdout=PIPE)

print (avc_lidar.last_sample)
