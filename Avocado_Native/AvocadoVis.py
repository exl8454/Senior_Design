# AvocadoVis.py
# Avocado's graphics visualizer

# Native Import
import time
import math

# Third-Party Import
import pygame

# Avocado Import
from LidarHandler import LidarHandler as Lidar

def remap(value, fmin, fmax, tmin, tmax):
    fspan = fmax - fmin
    tspan = tmax - tmin

    scaled = float(value - fmin) / float(fspan)

    return tmin + (scaled * tspan)
def intensity(node):
    intensity = node[1]
    if intensity > 30:
        intensity = 30
    intensity /= 30 # Suppose to be max 100; never reaches tho
    red = (0 * intensity) + 0
    green = (255 * intensity) + 0
    blue = (-255 * intensity) + 255
    return (red, green, blue)

def getRect(angle, dist):
    rad = math.radians(angle)
    if dist == 0:
        return [300, 300]
    x = dist * math.cos(rad)
    y = dist * math.sin(rad)
    x = remap(x, 0, 6000, -3000, 3000)
    y = remap(y, 0, 6000, -3000, 3000)
    x = remap(x, -3000, 3000, 0, 300)
    y = remap(y, -3000, 3000, 0, 300)
    x += 300
    y += 300
    
    return [x, y]

def fullLine(nodes):
    node_size = len(nodes)
    i = 0
    for node in nodes:
        if i > node_size - 3:
            break;
        
        if node[3] == 0:
            i += 1
            pass
        else:
            start = getRect(node[2], node[3])
            next_node = nodes[i + 1]
            if next_node[3] == 0:
                next_node = node
            end = getRect(next_node[2], next_node[3])
            pygame.draw.line(screen, BLACK, start, end)
            i += 1

    last_node = nodes[node_size - 1]
    start = getRect(node[2], node[3])
    first_node = nodes[0]
    end = getRect(next_node[2], next_node[3])
    pygame.draw.line(screen, BLACK, start, end)
    return

def fullPoint(nodes):
    for node in nodes:
        if node[3] == 0:
            pass
        else:
            center = getRect(node[2], node[3])
            pygame.draw.rect(screen, intensity(node), [center[0] - 2, center[1] + 2, 2, 2])
    return

def singlePoint(node):
    i = 0
    while i < 540:
        if node[3] == 0:
            pass
        else:
            center = getRect(node[2], node[3])
            pygame.draw.rect(screen, intensity(node), [center[0] - 2, center[1] + 2, 2, 2])
        i += 1
        node = lidar.getNode()
    return

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

done = False
lidar = Lidar("COM5", 512)
time.sleep(1)
nodes = None
node = None

clock = pygame.time.Clock()

pygame.init()

size = (600, 600)
pygame.display.set_caption("Avocado Visualizer")
screen = pygame.display.set_mode(size)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill(WHITE)

    # Single-point continuous display points
    singlePoint(lidar.getNode())

    # Full scan display points
    #fullPoint(lidar.getFullScan())

    # Full scan display lines
    #fullLine(lidar.getFullScan())
    
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
