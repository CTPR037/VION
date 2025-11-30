import pygame
import shared
from screenScaling import *

clock = pygame.time.Clock()

def Update():
    shared.layers = sorted(shared.layers, key = lambda x : x[1], reverse = True)
    for surface, i, x, y in shared.layers:
        shared.screen.blit(surface, (x, y))
    # print(len(shared.layers))
    shared.layers.clear()
    DrawScaled()
    pygame.display.flip()
    clock.tick(180)
    # print('fps:', clock.get_fps())
