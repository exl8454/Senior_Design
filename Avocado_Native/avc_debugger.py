# avc_debugger.py
# Debugging script (Scratch)

from avc_servo import AvcServo as AS
from avc_file import AvcFile as AF
from avc_logger import AvcLogger as AL
from avc_data import AvcData as AD
from avc_lidar import AvcLidar as Lidar
from avc_servo import AvcServo as Servo
from avc_vis import AvcVis as AV

log = AL("AVC_DATA", 0, 'w')
dat = AD("AVC_DATA", 0, 'w')
file = AF(log, dat)
servo = Servo("COM7")
lidar = Lidar("COM11", 512, file, servo)
lidar.open()

vis = AV(lidar)
vis.startgfx()
