# File handler.py
# Handles file I/O

# Native Import
import os

# Avocado Import
import AvocadoLogger as logger

# Opens file from target directory and returns file object
# By default, file will be opened as read-only mode
def openFile(directory, mode = "r"):
    try:
        target = open(directory, mode)
        return target
    except IOError as ioe:
        logger.printErr("\/ File I/O Error \/")
        logger.printErr(">From openFile")
        logger.printErr(">In FileHandler.py")
        logger.printErr(ioe)
        return None
    
