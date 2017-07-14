# LidarParser.py
# Parses RPLidar data

import re # Regular Expression
import StreamHandler
import datetime

# Parses incoming data
# Once parsed, data is buffered into buffer variable
# Buffer variable is updated constantly
def ParseData(data):
    global output, buffer

    parsed = str(data.decode('utf-8'))
    for char in parsed:
        if (char >= '0') and (char <= '9'):
            output += char
        elif (char >= ' A') and (char <= 'Z'):
            output += char
        elif (char >= ' a') and (char <= 'z'):
            output += char
        elif (char >= '+') and (char <= '.'):
            output += char
        elif (char >= '[') and (char <= ']'):
            output += char

    # Dump to dumpfile
    output = output.replace("[0m", "")
    output = output.replace("[INFO]", "")

    if len(output.split("::")) > 1:
        timestamp = output.split("::")[0]
        timestamp = timestamp.replace("[", "")
        timestamp = timestamp.replace("]", "")
        angle = output.split("::")[1].split(",")[0]
        angle = angle.replace("[", "")
        dist = output.split("::")[1].split(",")[1]
        dist = dist.replace("]", "")

        timestamp = datetime.datetime.fromtimestamp(float(timestamp))
        output = "TIME=" + str(timestamp) + ",ANGLE=" + angle + ",DIST=" + dist

        buffer = output

    output = ""

def GetData():
    return buffer

output = ""
buffer = ""
