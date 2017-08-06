# AStar

from Node import Node

class AStar(object):

    PATH = None

    openList = None
    closedList = None
    
    def __init__(self):
        return

    def getAdjascent(self, node):
        nodes = None
        for i in range(node.X - 1, node.X + 2, 1):
            for j in range(node.Y - 1, node.Y + 2, 1):
                if (i != node.X) and (j != node.Y):
                    nodes.insert(len(nodes), Node(i, j))

        return nodes

    def findPath(self, x1, y1, x2, y2):
        # Reset PATH
        self.PATH = None
        # Create start point
        start = Node(x1, y1)
        # Create stop point
        stop = Node(x2, y2)
        # Put start point into closed list
        self.openList.insert(len(openList), start)
        
        while not(:
            # Get last node from closed list
            parent = closedList[-1]
            # Get surrounding adjascent nodes and add them to open list
            self.openList.append(getAdjascent(parent))
            pass
        return self.PATH
