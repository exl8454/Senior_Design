# AvocadoVis.py
# Avocado's graphics visualizer

# Native Import
import time
import math

# Third-Party Import
import pygame

# Avocado Import
from LidarHandler import LidarHandler as Lidar

def getRect(angle, dist):
    rad = math.radians(angle)
    if dist == 0:
        return [350, 350]
    x = 350 + (((dist * math.cos(rad)) / 6000) * 300)
    y = 350 + (((dist * math.sin(rad)) / 6000) * 300)
    return [x, y]

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

done = False

lidar = Lidar("COM11")
time.sleep(1)
nodes = lidar.getFullScan()

clock = pygame.time.Clock()

pygame.init()

size = (700, 700)
pygame.display.set_caption("Avocado Visualizer")
screen = pygame.display.set_mode(size)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    node_size = len(nodes)
    
    screen.fill(WHITE)
    i = 0
    j = 1

    for node in nodes:
        if i > node_size - 2:
            break;
        start = getRect(node[2], node[3])
        next_node = nodes[i + 1]
        end = getRect(next_node[2], next_node[3])
        pygame.draw.line(screen, BLACK, start, end)
        i += 1

    last_node = nodes[node_size - 1]
    start = getRect(node[2], node[3])
    first_node = nodes[0]
    end = getRect(next_node[2], next_node[3])
    pygame.draw.line(screen, BLACK, start, end)

    '''
    for node in nodes:
        center = getRect(node[2], node[3])
        pygame.draw.rect(screen, BLACK, [center[0] - 1, center[1] + 1, center[0] + 1, center[1] - 1])
    '''
        
    #pygame.draw.line(screen, BLACK, [300, 300], [400, 300])
    #pygame.draw.line(screen, BLACK, [400, 300], [400, 400])
    #pygame.draw.line(screen, BLACK, [400, 400], [300, 400])
    #pygame.draw.line(screen, BLACK, [300, 400], [300, 300])
    
    pygame.display.flip()
    clock.tick(120)

    nodes = lidar.getFullScan()

pygame.quit()
