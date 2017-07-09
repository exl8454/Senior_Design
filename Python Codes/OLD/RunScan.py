import sys, os
import subprocess

# For running Scanning input
rtncode = subprocess.Popen(['pwd'], shell = True, stdout = subprocess.PIPE)
rtncode = subprocess.Popen(['ls', '-a'], shell = True, stdout = subprocess.PIPE)
proc = subprocess.Popen('./runpy-2.sh', bufsize = -1, stdout = subprocess.PIPE)
while(True):
    line = proc.stdout.readline()
    parsed = str(line, 'utf-8')
    splits = parsed.split(": : ")
    if len(splits) > 1:
        timestamp = splits[0].split("\x1b[0m[ INFO] [")[1].split(']')
        angledist = splits[1].split("\x1b[0m\n")
        angle = angledist[0].split("[")[1].split(",")[0]
        dist = angledist[0].split(",")[1].split("]")[0]
        #print ("Split size:", len(splits), " ", splits[0], " ", splits[1])
        print ("TIME: ", timestamp[0], " ANGL: ", angle, " DIST: ", dist)

#print (proc.communicate()[0].decode('utf-8'))
