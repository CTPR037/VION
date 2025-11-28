import pygame
import shared

def MousePos():
    xRate = shared.letterbox.get_size()[0] / shared.screen.get_size()[0]
    yRate = shared.letterbox.get_size()[1] / shared.screen.get_size()[1]
    scaleRate = min((xRate, yRate))
    xOffset, yOffset = 0, 0
    if scaleRate == yRate: # 좌우 레터박스
        xOffset = (shared.letterbox.get_size()[0] - shared.screen.get_size()[0] * scaleRate) / 2
    else: # 상하 레터박스
        yOffset = (shared.letterbox.get_size()[1] - shared.screen.get_size()[1] * scaleRate) / 2
    mousePos = pygame.mouse.get_pos()
    mousePos = (mousePos[0] / scaleRate + xOffset - 960, 540 - (mousePos[1] / scaleRate + yOffset))
    # print(mousePos)
    return mousePos