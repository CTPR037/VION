import pygame
pygame.init()
pygame.key.stop_text_input()
import shared

pygame.display.set_caption("VION")
shared.screen = pygame.Surface((shared.BASE_WIDTH, shared.BASE_HEIGHT))
shared.gameScreen = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT))
info = pygame.display.Info()
shared.letterbox = pygame.display.set_mode((info.current_w, info.current_h))
pygame.mixer.init()
pygame.mixer.set_num_channels(32)


from images import *
from title import *
from lobby import *
from ingame import *
from screenScaling import *


shared.scene = 'Title'
shared.screen.fill((0, 0, 0))

while shared.userData['First']:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('click')
            shared.userData['First'] = 0
            with open('userdata.json', 'w', encoding='utf-8') as f:
                json.dump(shared.userData, f, ensure_ascii=False, indent=4)
    shared.layers.append((images['UI']['Tutorial'], 0, 0, 0))
    Update()

while True:
    if shared.scene == 'Title':
        Title()
    elif shared.scene == 'Lobby':
        Lobby()
    elif shared.scene == 'Ingame':
        Ingame()

pygame.quit()
exit()
