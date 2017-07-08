# LidarParser.py
# Parses RPLidar data

import StreamHandler

def ParseData(data):
    global parsed
    global output

    parsed = str(data)
    for char in parsed:
        if (char >= ' ') and (char <= '~'):
            output += char

    # Dump to dumpfile
    StreamHandler.writeData(output)

parsed = None
output = ""
