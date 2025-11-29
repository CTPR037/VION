import pygame
import time
import shared
from images import *
from update import *

def Title():
    import pygame.freetype
    y = 0
    scale = 3
    textY = -110
    startTime = time.perf_counter()
    fade = pygame.Surface((shared.BASE_WIDTH, shared.BASE_HEIGHT), pygame.SRCALPHA)
    while True:
        shared.events = pygame.event.get()
        for event in shared.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if time.perf_counter() - startTime > 1:
            y += (10 - y) * 0.1
            textY += (-130 - textY) * 0.1
            font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 30)
            font = font.render('by CTPR', (255, 255, 255), None)[0]
            shared.layers.append((font, 0, 0 - font.get_width() / 2 + 960, 540 - textY - font.get_height() / 2))
        
        scale += (1 - scale) * 0.1
        image = images['UI']['Title']
        newSize = (int(image.get_width() * scale), int(image.get_height() * scale))
        scaled = pygame.transform.scale(image, newSize)
        shared.layers.append((scaled, 0, -10 - scaled.get_width() / 2 + 960, 540 - y - scaled.get_height() / 2))
        shared.screen.fill((0, 0, 0))

        if time.perf_counter() - startTime > 1.5:
            fade.fill((255, 255, 255, (255 * (time.perf_counter() - startTime - 1.5)) if time.perf_counter() - startTime - 1.5 <= 1 else 255))
            shared.layers.append((fade, 0, 0, 0))
        if time.perf_counter() - startTime > 3:
            break
        Update()

    shared.scene = 'Lobby'