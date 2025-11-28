import pygame
import shared

def DrawScaled():
    screenW, screenH = shared.screen.get_size()
    baseW, baseH = shared.letterbox.get_size()

    scale = min(baseW / screenW, baseH / screenH)
    scaledW, scaledH = int(screenW * scale), int(screenH * scale)

    if screenW != shared.GAME_WIDTH:
        scaledScreen = pygame.transform.smoothscale(shared.screen, (scaledW, scaledH))
    else:
        scaledScreen = pygame.transform.scale(shared.screen, (scaledW, scaledH))

    x = (baseW - scaledW) // 2
    y = (baseH - scaledH) // 2

    shared.letterbox.fill((0, 0, 0))
    shared.letterbox.blit(scaledScreen, (x, y))
    