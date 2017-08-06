# Node

class Node(object):

    # Position
    X = 0
    Y = 0

    #F = G + H
    F = 0
    G = 0
    H = 0

    # Node object of parent
    parent = None

    def __init__(self, x, y):
        self.X = x
        self.Y = y
        return
