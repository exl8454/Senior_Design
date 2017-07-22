# avc_vis.py
# Re-deisnged class structure for AvocadoVis.py

# Native Import
import time
import math

# Thrid-Part Import
import pygame

# Avocado Import
from LidarHandler import LidarHandler as Lidar
import AvocadoLogger as logger

class AvcVis(object):
    BLACK = (  0,   0,   0)
    RED   = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLUE  = (  0,   0, 255)
    WHITE = (255, 255, 255)
    done = False
    lidar = None
    nodes = None
    node = None
    clock = pygame.time.Clock()
    size = (600, 600)
    screen = None

    def __init__(self, lidar):
        self.lidar = lidar
        if self.lidar is None:
            logger.printInfo("From avc_vis: LIDAR IS NOT SET")

        return

    def startgfx(self):
        pygame.init()
        pygame.display.set_caption("Avocado Visualizer")
        self.screen = pygame.display.set_mode(self.size)
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.screen.fill(self.WHITE)

            self.singlePoint(self.lidar.getNode(True), 361)

            pygame.display.flip()
            self.clock.tick()

        pygame.quit()
        self.done = False
            
    def remap(self, value, fmin, fmax, tmin, tmax):
        fspan = fmax - fmin
        tspan = tmax - tmin

        scaled = float(value - fmin) / float(fspan)

        return tmin + (scaled * tspan)

    def intensity(self, node, lim = 100):
        intensity = node[1]
        if intensity > lim:
            intensity = lim

        intensity /= lim

        red = (0 * intensity) + 0
        green = (255 * intensity) + 0
        blue = (-255 * intensity) + 255
        return (red, green, blue)

    def getRect(self, angle, dist):
        radian = math.radians(angle)
        if dist == 0:
            return [300, 300]

        x = dist * math.cos(radian)
        y = dist * math.sin(radian)

        x = self.remap(x, 0, 6000, 0, 300)
        y = self.remap(y, 0, 6000, 0, 300)

        x += 300
        y += 300

        return [x, y]

    def singlePoint(self, node, sampling):
        i = 0
        while i <= sampling:
            if node[3] == 0:
                pass
            else:
                center = self.getRect(node[2], node[3])
                pygame.draw.rect(self.screen, self.intensity(node, 35), [center[0] - 2, center[1] + 2, 2, 2])

                # Orientation
                if 91 >= node[2] and node[2] >= 89:
                    pygame.draw.line(self.screen, self.GREEN, [center[0], center[1]], [300, 300])
                if 181 >= node[2] and node[2] >= 179:
                    pygame.draw.line(self.screen, self.BLUE, [center[0], center[1]], [300, 300])
                if 271 >= node[2] and node[2] >= 269:
                    pygame.draw.line(self.screen, self.BLACK, [center[0], center[1]], [300, 300])
                if (360 >= node[2] and node[2] >= 359):
                    pygame.draw.line(self.screen, self.RED, [center[0], center[1]], [300, 300])
                elif (1 >= node[2] and node[2] >= 0):
                    pygame.draw.line(self.screen, self.RED, [center[0], center[1]], [300, 300])
            i += 1
            node = self.lidar.getNode(True)
        return
