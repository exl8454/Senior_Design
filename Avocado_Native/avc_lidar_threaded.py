# Threaded LIDAR Handler

# Native Import
import threading

# Third-Party Import
import serial

#Avocado Import

class Lidar(threading.Thread):

    isRunning = False

    def __init__(self, thread_name):
        threading.Thread.__init__(self, name = thread_name)
        return

    def run(self):
        self.isRunning = True
        while self.isRunning:
            pass
        return

    def stop(self):
        self.isRunning = False
        return
