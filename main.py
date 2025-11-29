import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "ffpyplayer"])
import pygame
pygame.init()
pygame.key.stop_text_input()
import shared

pygame.display.set_caption("VION")
shared.screen = pygame.Surface((shared.BASE_WIDTH, shared.BASE_HEIGHT))
shared.gameScreen = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT))
info = pygame.display.Info()
shared.letterbox = pygame.display.set_mode((info.current_w, info.current_h))
pygame.mixer.init(buffer=256)
pygame.mixer.set_num_channels(10)


from images import *
from title import *
from lobby import *
from ingame import *
from screenScaling import *


shared.scene = 'Title'
shared.screen.fill((0, 0, 0))

# time.sleep(1)
while True:
    if shared.scene == 'Title':
        Title()
    elif shared.scene == 'Lobby':
        Lobby()
    elif shared.scene == 'Ingame':
        Ingame()

pygame.quit()
exit()
