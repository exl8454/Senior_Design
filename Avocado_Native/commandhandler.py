# commandhandler.py
# Handles commands

# Native Imports
import threading

# Third-party Imports

# Avocado Imports

class CommandHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        return

    def run(self):
        command = input("AVOCADO>>>")
        while not(command in ['exit']):
            command = input("ACOVADO>>>")
