import pygame
import time
import math
import shared
import json
from images import *
from update import *
from mouse import *
from ffpyplayer.player import MediaPlayer
from motion import *

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.rot = 0
camera = Camera()

def DrawImage(image, x, y, z, rot, scale):
    newX = x - camera.x
    newY = y - camera.y
    shared.layers.append((image, 1, newX - image.get_width() / 2 + shared.screen.get_size()[0] / 2, shared.screen.get_size()[1] / 2 - newY - image.get_height() / 2))
    
    # if z - camera.z <= 0:
    #     return

    # scale *= 1 / (z - camera.z)
    # newSize = (int(image.get_width() * scale), int(image.get_height() * scale))
    # if scale == 1:
    #     scaled = image
    # else:
    #     scaled = pygame.transform.scale(image, newSize)
    # if rot == 0 and camera.rot == 0:
    #     rotated = scaled
    # else:
    #     rotated = pygame.transform.rotate(scaled, -rot + camera.rot)

    # newX = ((x - camera.x) * math.cos(math.radians(camera.rot)) - (y - camera.y) * math.sin(math.radians(camera.rot))) / (z - camera.z)
    # newY = ((x - camera.x) * math.sin(math.radians(camera.rot)) + (y - camera.y) * math.cos(math.radians(camera.rot))) / (z - camera.z)
    
    # shared.layers.append((rotated, z, newX - rotated.get_width() / 2 + shared.screen.get_size()[0] / 2, shared.screen.get_size()[1] / 2 - newY - rotated.get_height() / 2))
    
def DrawPolygon(points, color, surface): # points -> (x,y,z)
    newPoints = []
    for x, y, z in points:
        if z - camera.z <= 0:
            return
        newX = ((x - camera.x) * math.cos(math.radians(camera.rot)) - (y - camera.y) * math.sin(math.radians(camera.rot))) / (z - camera.z)
        newY = ((x - camera.x) * math.sin(math.radians(camera.rot)) + (y - camera.y) * math.cos(math.radians(camera.rot))) / (z - camera.z)
        newPoints.append((newX + 640, 360 - newY))
    pygame.draw.polygon(surface, color, newPoints)


class PlayArea:
    def __init__(self):
        self.startLine = [0, 360, 1]
        self.endLine = [0, -360, 1]
        self.checkLine = (0, -240, 1)
        self.areaSurface = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT), pygame.SRCALPHA)
        self.effectSurface = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT), pygame.SRCALPHA)
        self.prevPressedKeys = pygame.key.get_pressed()
        self.effectTime = [('tap', 0), ('tap', 0), ('tap', 0), ('tap', 0)]
        
    def Update(self):
        self.checkLine = ((self.startLine[0] * 1 + self.endLine[0] * 3) / 4, 
                          (self.startLine[1] * 1 + self.endLine[1] * 3) / 4, 
                          (self.startLine[2] * 1 + self.endLine[2] * 3) / 4)
        xangle = math.atan2(self.startLine[1] - self.checkLine[1], self.startLine[0] - self.checkLine[0])
        angle = math.atan2(self.startLine[1] - self.checkLine[1], self.startLine[2] - self.checkLine[2])
        
        self.areaSurface.fill((0, 0, 0, 0))
        start1 = (self.startLine[0] - 200, self.startLine[1], self.startLine[2])
        start2 = (self.startLine[0] + 200, self.startLine[1], self.startLine[2])
        end1 = (self.endLine[0] - 200, self.endLine[1], self.endLine[2])
        end2 = (self.endLine[0] + 200, self.endLine[1], self.endLine[2])
        DrawPolygon((start1, start2, end2, end1), colors[shared.songList[shared.curSongIdx]]['PlayArea'], self.areaSurface)
        
        checkLine1 = (self.checkLine[0] + 7 * math.cos(xangle), 
                      self.checkLine[1] + 7 * math.sin(angle), 
                      self.checkLine[2] + 7 * math.cos(angle))
        checkLine2 = (self.checkLine[0] - 7 * math.cos(xangle), 
                      self.checkLine[1] - 7 * math.sin(angle), 
                      self.checkLine[2] - 7 * math.cos(angle))
        check1 = (checkLine1[0] - 200, checkLine1[1], checkLine1[2])
        check2 = (checkLine1[0] + 200, checkLine1[1], checkLine1[2])
        check3 = (checkLine2[0] - 200, checkLine2[1], checkLine2[2])
        check4 = (checkLine2[0] + 200, checkLine2[1], checkLine2[2])
        DrawPolygon((check1, check2, check4, check3), colors[shared.songList[shared.curSongIdx]]['CheckLine'], self.areaSurface)
        
        # self.effectSurface.fill((0, 0, 0, 0))
        # keys = (pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k, pygame.K_e, pygame.K_r, pygame.K_u, pygame.K_i)
        # pressedKeys = []
        # for event in shared.events:
        #     if event.type == pygame.KEYDOWN:
        #         pressedKeys.append(event.key)
        # for i in range(4):
        #     if keys[i] in pressedKeys:
        #         self.effectTime[i] = ('tap', time.perf_counter())
        #     if keys[i+4] in pressedKeys:
        #         self.effectTime[i] = ('flick', time.perf_counter())
        #     if time.perf_counter() - self.effectTime[i][1] < 0.1:
        #         p1 = (self.startLine[0] - 200 + 100 * i, self.startLine[1], self.startLine[2])
        #         p2 = (self.startLine[0] - 100 + 100 * i, self.startLine[1], self.startLine[2])
        #         p3 = (self.endLine[0] - 200 + 100 * i, self.endLine[1], self.endLine[2])
        #         p4 = (self.endLine[0] - 100 + 100 * i, self.endLine[1], self.endLine[2])
        #         if self.effectTime[i][0] == 'tap':
        #             effectColor = colors[shared.songList[shared.curSongIdx]]['TapNote']
        #         else:
        #             effectColor = colors[shared.songList[shared.curSongIdx]]['FlickNote']
        #         effectColor = (effectColor[0], effectColor[1], effectColor[2], 50 - 50 * (time.perf_counter() - self.effectTime[i][1]) / 0.1)
        #         DrawPolygon((p1, p2, p4, p3), effectColor, self.effectSurface)
        
        shared.layers.append((self.areaSurface, 1, 0, 0))
        # shared.layers.append((self.effectSurface, 0.5, 0, 0))
playArea = PlayArea()


noteSurface = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT), pygame.SRCALPHA)
effectSurface = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT), pygame.SRCALPHA)
class Note:
    def __init__(self, type, key, startTime, offset):
        self.type = type
        self.key = key
        self.bpm = shared.charts[shared.songList[shared.curSongIdx]][shared.difficulty]["bpm"]
        self.startTime = startTime * 60 / self.bpm + offset
        self.offset = offset
        self.progress = 0
        self.hit = 0
        self.missed = False
    def Update(self):
        self.progress = (time.perf_counter() - self.startTime) / shared.settings['noteSpeed'] # 0~1
    
class TapNote(Note):
    def __init__(self, key, startTime, offset):
        super().__init__('TapNote', key, startTime, offset)
        
    def Update(self):
        super().Update()
        if self.key == 'd':
            x = -150
        elif self.key == 'f':
            x = -50
        elif self.key == 'j':
            x = 50
        elif self.key == 'k':
            x = 150
        startX = playArea.startLine[0] + x
        startY = playArea.startLine[1]
        startZ = playArea.startLine[2]
        checkX = playArea.checkLine[0] + x
        checkY = playArea.checkLine[1]
        checkZ = playArea.checkLine[2]
        x = startX + (checkX - startX) * self.progress
        y = startY + (checkY - startY) * self.progress
        z = startZ + (checkZ - startZ) * self.progress
        xangle = math.atan2(startY - checkY, startX - checkX)
        angle = math.atan2(startY - checkY, startZ - checkZ)
        p1 = (x + 7 * math.cos(xangle) - 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
        p2 = (x + 7 * math.cos(xangle) + 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
        p3 = (x - 7 * math.cos(xangle) - 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
        p4 = (x - 7 * math.cos(xangle) + 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
        DrawPolygon((p1, p2, p4, p3), colors[shared.songList[shared.curSongIdx]]['TapNote'], noteSurface) # 180, 240, 255

class HoldNote(Note):
    def __init__(self, key, startTime, endTime, offset):
        super().__init__('HoldNote', key, startTime, offset)
        self.endTime = endTime * 60 / self.bpm + offset
        self.endProgress = 0
        self.endMissed = False
        self.startHit = False
        self.holdCheckTime = []
        time = startTime + 0.25
        while time < endTime - 0.25:
            self.holdCheckTime.append(time * 60 / self.bpm + offset)
            time += 0.25
    def Update(self):
        super().Update()
        self.endProgress = (time.perf_counter() - self.endTime) / shared.settings['noteSpeed']
        if self.key == 'd':
            x = -150
        elif self.key == 'f':
            x = -50
        elif self.key == 'j':
            x = 50
        elif self.key == 'k':
            x = 150
        startX = playArea.startLine[0] + x
        startY = playArea.startLine[1]
        startZ = playArea.startLine[2]
        checkX = playArea.checkLine[0] + x
        checkY = playArea.checkLine[1]
        checkZ = playArea.checkLine[2]
        xangle = math.atan2(startY - checkY, startX - checkX)
        angle = math.atan2(startY - checkY, startZ - checkZ)

        if self.endProgress < 1: # 중간
            if self.progress < 1: # 중간시작
                sx = startX + (checkX - startX) * self.progress
                sy = startY + (checkY - startY) * self.progress
                sz = startZ + (checkZ - startZ) * self.progress
            else:
                sx = checkX
                sy = checkY
                sz = checkZ
            if self.endProgress >= 0: # 중간끝
                ex = startX + (checkX - startX) * self.endProgress
                ey = startY + (checkY - startY) * self.endProgress
                ez = startZ + (checkZ - startZ) * self.endProgress
            else:
                ex = startX
                ey = startY
                ez = startZ
            p1 = (sx - 30, sy, sz)
            p2 = (sx + 30, sy, sz)
            p3 = (ex - 30, ey, ez)
            p4 = (ex + 30, ey, ez)
            DrawPolygon((p1, p2, p4, p3), colors[shared.songList[shared.curSongIdx]]['HoldNote'], noteSurface)

        if self.endProgress < 1:
            if self.progress < 1: # 시작
                x = startX + (checkX - startX) * self.progress
                y = startY + (checkY - startY) * self.progress
                z = startZ + (checkZ - startZ) * self.progress
            else:
                x = checkX
                y = checkY
                z = checkZ
            p1 = (x + 7 * math.cos(xangle) - 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
            p2 = (x + 7 * math.cos(xangle) + 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
            p3 = (x - 7 * math.cos(xangle) - 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
            p4 = (x - 7 * math.cos(xangle) + 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
            DrawPolygon((p1, p2, p4, p3), colors[shared.songList[shared.curSongIdx]]['TapNote'], noteSurface)
        
        if self.endProgress >= 0: # 끝
            x = startX + (checkX - startX) * self.endProgress
            y = startY + (checkY - startY) * self.endProgress
            z = startZ + (checkZ - startZ) * self.endProgress
            p1 = (x + 7 * math.cos(xangle) - 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
            p2 = (x + 7 * math.cos(xangle) + 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
            p3 = (x - 7 * math.cos(xangle) - 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
            p4 = (x - 7 * math.cos(xangle) + 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
            DrawPolygon((p1, p2, p4, p3), colors[shared.songList[shared.curSongIdx]]['TapNote'], noteSurface)

class FlickNote(Note):
    def __init__(self, key, startTime, offset):
        super().__init__('FlickNote', key, startTime, offset)
        
    def Update(self):
        super().Update()
        if self.key == 'd':
            x = -150
        elif self.key == 'f':
            x = -50
        elif self.key == 'j':
            x = 50
        elif self.key == 'k':
            x = 150
        startX = playArea.startLine[0] + x
        startY = playArea.startLine[1]
        startZ = playArea.startLine[2]
        checkX = playArea.checkLine[0] + x
        checkY = playArea.checkLine[1]
        checkZ = playArea.checkLine[2]
        x = startX + (checkX - startX) * self.progress
        y = startY + (checkY - startY) * self.progress
        z = startZ + (checkZ - startZ) * self.progress
        xangle = math.atan2(startY - checkY, startX - checkX)
        angle = math.atan2(startY - checkY, startZ - checkZ)
        p1 = (x + 7 * math.cos(xangle) - 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
        p2 = (x + 7 * math.cos(xangle) + 40, y + 7 * math.sin(angle), z + 7 * math.cos(angle))
        p3 = (x - 7 * math.cos(xangle) - 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
        p4 = (x - 7 * math.cos(xangle) + 40, y - 7 * math.sin(angle), z - 7 * math.cos(angle))
        DrawPolygon((p1, p2, p4, p3), colors[shared.songList[shared.curSongIdx]]['FlickNote'], noteSurface) # 180, 240, 255
        import colorsys
        color = colors[shared.songList[shared.curSongIdx]]['FlickNote']
        color = colorsys.rgb_to_hls(color[0]/255, color[1]/255, color[2]/255)
        color = colorsys.hls_to_rgb(color[0], color[1]-0.2, color[2])
        color = (color[0]*255, color[1]*255, color[2]*255)
        effectY = time.perf_counter() % 0.5 * 2 * 25
        p1 = (x, y + 30 + effectY, z)
        p2 = (x, y + 15 + effectY, z)
        p3 = (x - 20, y + 15 + effectY, z)
        p4 = (x - 20, y + effectY, z)
        p5 = (x + 20, y + 15 + effectY, z)
        p6 = (x + 20, y + effectY, z)
        DrawPolygon((p1, p5, p6, p2, p4, p3), (color[0], color[1], color[2], 255 - effectY / 25 * 255), effectSurface)

class HitEffect:
    def __init__(self, key, type):
        self.key = key
        self.type = type
        self.scale = 1
        self.alpha = 127
        self.startTime = time.perf_counter()
        self.progress = 0
    def Update(self):
        x = 0
        if self.key == 'd':
            x = -150
        elif self.key == 'f':
            x = -50
        elif self.key == 'j':
            x = 50
        elif self.key == 'k':
            x = 150
        x += playArea.checkLine[0]
        y = playArea.checkLine[1]
        z = playArea.checkLine[2]
        self.progress = (time.perf_counter() - self.startTime) / 0.5
        self.scale = 1 + 1 * (1 - ((self.progress - 1) ** 4))
        self.alpha = 255 - 255 * (1 - ((self.progress - 1) ** 4))
        p1 = (x, y + 35 * self.scale, z)
        p2 = (x + 35 * self.scale, y, z)
        p3 = (x, y - 35 * self.scale, z)
        p4 = (x - 35 * self.scale, y, z)
        color = colors[shared.songList[shared.curSongIdx]]['FlickNote' if self.type == 'FlickNote' else 'TapNote']
        color = (color[0], color[1], color[2], self.alpha if self.progress <= 1 else 0)
        DrawPolygon((p1, p2, p3, p4), color, effectSurface)

class ScoreText:
    def __init__(self):
        self.accuracy = ''
        self.fastSlow = ''
        self.startTime = 0
        self.size = 1
        self.score = 0
        self.isPerfect = True
        self.isFullCombo = True
        self.noteNum = 0
        self.holdNum = 0
        self.perfectCnt = 0
        self.greatCnt = 0
        self.goodCnt = 0
        self.missCnt = 0
        self.combo = 0
        
    def Update(self):
        import pygame.freetype
        if time.perf_counter() - self.startTime < 1:
            self.size += (1 - self.size) * 0.1
            if self.accuracy == 'GREAT' or self.accuracy == 'GOOD':
                color = (200, 200, 255) if self.fastSlow == 'fast' else (255, 200, 200)
            elif self.accuracy == 'MISS':
                color = (200, 200, 200)
            else:
                color = (255, 255, 255)
            font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 30 * self.size).render(self.accuracy, color, None)[0]
            DrawImage(font, 0, -25, 1, 0, 1)
        font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 15).render('COMBO', (200, 200, 200), None)[0]
        DrawImage(font, 0, 55, 1, 0, 1)
        font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 45).render(f'{self.combo}', (255, 255, 255), None)[0]
        DrawImage(font, 0, 25, 1, 0, 1)
        font = pygame.freetype.Font("font/Pretendard-Medium.ttf", 25).render(f'{round(self.score):,}', (255, 255, 255), None)[0]
        DrawImage(font, 0, 310, 1, 0, 1)
        if self.isPerfect:
            color = (127, 255, 255, 200)
        elif self.isFullCombo:
            color = (200, 255, 255, 200)
        if self.isFullCombo:
            p1 = (-70, 35, 1)
            p2 = (-60, 25, 1)
            p3 = (-70, 15, 1)
            p4 = (-80, 25, 1)
            DrawPolygon((p1, p2, p3, p4), color, effectSurface)
            p1 = (70, 35, 1)
            p2 = (60, 25, 1)
            p3 = (70, 15, 1)
            p4 = (80, 25, 1)
            DrawPolygon((p1, p2, p3, p4), color, effectSurface)

    def Show(self, accuracy, fastSlow = '', hold = False):
        self.accuracy = accuracy
        self.fastSlow = fastSlow
        self.startTime = time.perf_counter()
        self.size = 1.3
        if self.accuracy == 'PERFECT':
            if hold:
                self.score += 500000 / (self.noteNum + self.holdNum / 2)
            else:
                self.score += 1000000 / (self.noteNum + self.holdNum / 2)
            self.perfectCnt += 1
            self.combo += 1
        elif self.accuracy == 'GREAT':
            self.score += 500000 / (self.noteNum + self.holdNum / 2)
            self.isPerfect = False
            self.greatCnt += 1
            self.combo += 1
        elif self.accuracy == 'GOOD':
            self.score += 250000 / (self.noteNum + self.holdNum / 2)
            self.isFullCombo = False
            self.isPerfect = False
            self.goodCnt += 1
            self.combo = 1
        else:
            self.isFullCombo = False
            self.isPerfect = False
            self.missCnt += 1
            self.combo = 0
scoreText = ScoreText()

def Gimmick(startTime):
    if shared.songList[shared.curSongIdx] == '염라':
        incline = [(60, 100)]
    if shared.songList[shared.curSongIdx] == '잔혹한 천사의 테제':
        incline = [(69, 91)]
    if shared.songList[shared.curSongIdx] == 'PPPP':
        incline = [(44.5, 60.5)]
    if shared.songList[shared.curSongIdx] == 'Flower Rocket':
        incline = [(25.5, 42), (75.5, 92), (134.5, 153), (172, 186)]
    if shared.songList[shared.curSongIdx] == 'danser':
        incline = [(32, 53), (61, 74)]
    for i in incline:
        s, e = i
        if s <= time.perf_counter() - startTime < s + 0.5:
                playArea.startLine[1] = 360 + 220 * EaseIn(startTime + s, 0.5)
                playArea.startLine[2] = 1 + 1 * EaseIn(startTime + s, 0.5)
                playArea.endLine[1] = -360 + 5 * EaseIn(startTime + s, 0.5)
                playArea.endLine[2] = 1 - 0.49 * EaseIn(startTime + s, 0.5)
        if s + 0.5 <= time.perf_counter() - startTime < s + 1:
                playArea.startLine[1] = 580 + 220 * EaseOut(startTime + s + 0.5, 0.5)
                playArea.startLine[2] = 2 + 1 * EaseOut(startTime + s + 0.5, 0.5)
                playArea.endLine[1] = -355 + 5 * EaseOut(startTime + s + 0.5, 0.5)
                playArea.endLine[2] = 0.51 - 0.5 * EaseOut(startTime + s + 0.5, 0.5)
        if s + 1 <= time.perf_counter() - startTime < s + 2:
            playArea.startLine[1] = 800
            playArea.startLine[2] = 3
            playArea.endLine[1] = -350
            playArea.endLine[2] = 0.01
        if e <= time.perf_counter() - startTime < e + 0.5:
                playArea.startLine[1] = 800 - 220 * EaseIn(startTime + e, 0.5)
                playArea.startLine[2] = 3 - 1 * EaseIn(startTime + e, 0.5)
                playArea.endLine[1] = -350 - 5 * EaseIn(startTime + e, 0.5)
                playArea.endLine[2] = 0.01 + 0.49 * EaseIn(startTime + e, 0.5)
        if e + 0.5 <= time.perf_counter() - startTime < e + 1:
                playArea.startLine[1] = 580 - 220 * EaseOut(startTime + e + 0.5, 0.5)
                playArea.startLine[2] = 2 - 1 * EaseOut(startTime + e + 0.5, 0.5)
                playArea.endLine[1] = -355 - 5 * EaseOut(startTime + e + 0.5, 0.5)
                playArea.endLine[2] = 0.5 + 0.5 * EaseOut(startTime + e + 0.5, 0.5)
        if e + 1 <= time.perf_counter() - startTime < e + 2:
            playArea.startLine[1] = 360
            playArea.startLine[2] = 1
            playArea.endLine[1] = -360
            playArea.endLine[2] = 1

def Ingame():
    import pygame.freetype
    songName = shared.songList[shared.curSongIdx]
    notesData = sorted(shared.charts[songName][shared.difficulty]["notes"], key = lambda x : x['time']) # 리스트
    bpm = shared.charts[songName][shared.difficulty]["bpm"]
    offset = shared.charts[songName][shared.difficulty]["offset"]
    bga = MediaPlayer(images[songName]['BGA'], ff_opts={'an': True})
    bgaSurface = None
    shared.songFiles[songName].set_volume(shared.settings['ingameMusicVol'])
    shared.sfxFiles['Hit'].set_volume(shared.settings['ingameSfxVol'])
    shared.sfxFiles['Flick'].set_volume(shared.settings['ingameSfxVol'])
    # camera = Camera()
    # playArea = PlayArea()
    scoreText = ScoreText()
    for note in notesData:
        if note['type'] == 'hold':
            scoreText.noteNum += 1 # 시작
            _ = 0
            while note['time'] + (_+1) * 0.25 < note['end'] - 0.25:
                _ += 1
            scoreText.holdNum += _ # 중간
            scoreText.noteNum += 1 # 끝
        else:
            scoreText.noteNum += 1
    PERFECT_RANGE = 0.05
    GREAT_RANGE = 0.1
    GOOD_RANGE = 0.15
    MISS_RANGE = 0.3
    keyMap = {'d' : pygame.K_d, 'f' : pygame.K_f, 'j' : pygame.K_j, 'k' : pygame.K_k, 'e' : pygame.K_e, 'r' : pygame.K_r, 'u' : pygame.K_u, 'i' : pygame.K_i}
    prevPressedKeys = pygame.key.get_pressed()
    holdingNotes = {'d':None, 'f':None, 'j':None, 'k':None}
    flickMap = {'d' : 'e', 'f' : 'r', 'j' : 'u', 'k' : 'i'}
    exitGame = False
    
    transition = time.perf_counter()
    fade = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT), pygame.SRCALPHA)
    shared.screen = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT))

    playArea.startLine = [0, 360, 1]
    playArea.endLine = [0, -360, 1]

    while True: # intro
        shared.events = pygame.event.get()
        for event in shared.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        shared.screen.fill((0, 0, 0))
        playArea.Update()

        if time.perf_counter() - transition <= 1:
            fade.fill((255, 255, 255, 255 * (1 - (time.perf_counter() - transition))))
            DrawImage(fade, 0, 0, 1, 0, 1)
        else:
            break
        Update()

    startTime = time.perf_counter()
    endTime = 0
    noteIdx = 0
    songPlay = False
    gameNotes = []
    hitEffects = []

    # playArea.startLine[1] = 800
    # playArea.startLine[2] = 3
    # playArea.endLine[1] = -350
    # playArea.endLine[2] = 0.01

    frame = None
    dark = pygame.Surface((shared.GAME_WIDTH, shared.GAME_HEIGHT), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 100))
    while True: # 
        shared.events = pygame.event.get()
        for event in shared.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exitGame = True
        if exitGame:
            break

        Gimmick(startTime)

        timer = time.perf_counter() - startTime
        shared.screen.fill((0, 0, 0))
        if timer >= shared.settings['noteSpeed']: # BGA
            if frame is None:
                frame, val = bga.get_frame()
            else:
                img, t = frame
                if t <= timer - shared.settings['noteSpeed']:
                    data = img.to_bytearray()[0]
                    w, h = img.get_size()
                    bgaSurface = pygame.image.frombuffer(data, (w, h), "RGB")
                    frame, val = bga.get_frame()
            if bgaSurface is not None:
                DrawImage(bgaSurface, 0, 0, 1, 0, 1)
        DrawImage(dark, 0, 0, 1, 0, 1)
        playArea.Update()

        if timer >= shared.settings['noteSpeed'] and not songPlay:
            shared.songFiles[songName].play()
            songPlay = True

        while noteIdx < len(notesData): # spawn
            currentNoteData = notesData[noteIdx]
            noteStartTime = currentNoteData['time'] * 60/bpm + offset + shared.settings['offset']
            if timer >= noteStartTime:
                if currentNoteData['type'] == 'tap':
                    gameNotes.append(TapNote(currentNoteData['key'], currentNoteData['time'], startTime + offset + shared.settings['offset']))
                if currentNoteData['type'] == 'hold':
                    gameNotes.append(HoldNote(currentNoteData['key'], currentNoteData['time'], currentNoteData['end'], startTime + offset + shared.settings['offset']))
                if currentNoteData['type'] == 'flick':
                    gameNotes.append(FlickNote(currentNoteData['key'], currentNoteData['time'], startTime + offset + shared.settings['offset']))
                noteIdx += 1
            else:
                break
        
        noteSurface.fill((0, 0, 0, 0))
        effectSurface.fill((0, 0, 0, 0))
        scoreText.Update()
        hitableNotes = {'d':[], 'f':[], 'j':[], 'k':[], 'e':[], 'r':[], 'u':[], 'i':[]}

        for note in gameNotes: # update / miss
            note.Update()
            if -GOOD_RANGE <= note.startTime + shared.settings['noteSpeed'] - time.perf_counter() <= MISS_RANGE:
                hitableNotes[flickMap[note.key] if note.type == 'FlickNote' else note.key].append((note, note.startTime + shared.settings['noteSpeed'] - time.perf_counter()))
            else:
                if note.type != 'HoldNote' and note.startTime + shared.settings['noteSpeed'] - time.perf_counter() < -GOOD_RANGE and not note.missed:
                    # print('MISS')
                    scoreText.Show('MISS')
                    note.missed = True
                elif note.type == 'HoldNote' and note.startTime + shared.settings['noteSpeed'] - time.perf_counter() < -GOOD_RANGE and not note.missed and not note.startHit:
                    scoreText.Show('MISS')
                    note.missed = True
                elif note.type == 'HoldNote' and note.endTime + shared.settings['noteSpeed'] - time.perf_counter() < -GOOD_RANGE and not note.endMissed:
                    # print('MISS')
                    scoreText.Show('MISS')
                    note.endMissed = True
                    holdingNotes[note.key] = None

        pressedKeys = {'d' : False, 'f' : False, 'j' : False, 'k' : False, 'e' : False, 'r' : False, 'u' : False, 'i' : False}
        for key in 'dfjkerui': # 판정
            if pygame.key.get_pressed()[keyMap[key]] and not prevPressedKeys[keyMap[key]]:
                pressedKeys[key] = True

            if hitableNotes[key] and pressedKeys[key]:
                hitableNotes[key].sort(key = lambda x : abs(x[1]))
                note = hitableNotes[key][0]

                if note[0].type != 'HoldNote':
                    note[0].hit = True

                if GOOD_RANGE < note[1] <= MISS_RANGE:
                    if not note[0].missed:
                        note[0].missed = True
                        scoreText.Show('MISS')
                        if note[0].type == 'HoldNote':
                            note[0].startHit = True
                else:
                    if not note[0].missed and not (note[0].type == 'HoldNote' and note[0].startHit):
                        if abs(note[1]) <= PERFECT_RANGE:
                            # print('PERFECT')
                            scoreText.Show('PERFECT')
                        elif abs(note[1]) <= GREAT_RANGE:
                            # print('GREAT', 'fast' if note[1] > 0 else 'slow')
                            scoreText.Show('GREAT', 'fast' if note[1] > 0 else 'slow')
                        else:
                            # print('GOOD', 'fast' if note[1] > 0 else 'slow')
                            scoreText.Show('GOOD', 'fast' if note[1] > 0 else 'slow')
                        if note[0].type == 'HoldNote':
                            note[0].startHit = True
                        hitEffects.append(HitEffect(note[0].key, note[0].type))
                        shared.sfxFiles['Flick' if note[0].type == 'FlickNote' else 'Hit'].play()
                        

            if hitableNotes[key] and hitableNotes[key][0][0].type == 'HoldNote' and hitableNotes[key][0][1] <= 0:
                holdingNotes[key] = hitableNotes[key][0][0]

            if key in 'dfjk' and holdingNotes[key]:
                if holdingNotes[key].hit < len(holdingNotes[key].holdCheckTime):
                    if time.perf_counter() >= holdingNotes[key].holdCheckTime[holdingNotes[key].hit] + shared.settings['noteSpeed']:
                        holdingNotes[key].hit += 1
                        if pygame.key.get_pressed()[keyMap[key]]:
                            # print('PERFECT')
                            scoreText.Show('PERFECT', hold = True)
                            hitEffects.append(HitEffect(key, 'HoldNote'))
                        else:
                            # print('MISS')
                            scoreText.Show('MISS', hold = True)
                else: # 홀드 떼는 판정
                    if not pygame.key.get_pressed()[keyMap[key]] and prevPressedKeys[keyMap[key]]:
                        holdingNotes[key].hit += 1
                        if abs(holdingNotes[key].endTime + shared.settings['noteSpeed'] - time.perf_counter()) <= PERFECT_RANGE:
                            # print('PERFECT')
                            scoreText.Show('PERFECT')
                        elif abs(holdingNotes[key].endTime + shared.settings['noteSpeed'] - time.perf_counter()) <= GREAT_RANGE:
                            scoreText.Show('GREAT', 'fast' if holdingNotes[key].endTime + shared.settings['noteSpeed'] - time.perf_counter() > 0 else 'slow')
                        else:
                            scoreText.Show('GOOD', 'fast' if holdingNotes[key].endTime + shared.settings['noteSpeed'] - time.perf_counter() > 0 else 'slow')
                        hitEffects.append(HitEffect(key, 'HoldNote'))
                        shared.sfxFiles['Hit'].play()
                        holdingNotes[key] = None

        prevPressedKeys = pygame.key.get_pressed()
        temp = []
        for note in gameNotes:
            if note.type != 'HoldNote':
                if note.progress <= 1.33 and note.hit == False and not (note.missed and note.progress < 1):
                    temp.append(note)
                elif note.progress > 1.33:
                    scoreText.Show('MISS')
            elif note.type == 'HoldNote':
                if note.endProgress <= 1.33 and note.hit <= len(note.holdCheckTime):
                    temp.append(note)
                elif note.endProgress > 1.33:
                    scoreText.Show('MISS', hold = True)

        gameNotes = temp.copy()
        # gameNotes = [note for note in gameNotes 
        #              if note.type != 'HoldNote' and note.progress <= 1.33 and note.hit == False and not (note.missed and note.progress < 1)
        #              or note.type == 'HoldNote' and note.endProgress <= 1.33 and note.hit <= len(note.holdCheckTime)]
        for eff in hitEffects:
            eff.Update()
        hitEffects = [e for e in hitEffects
                      if e.progress < 1]

        shared.layers.append((noteSurface, 1, 0, 0))
        shared.layers.append((effectSurface, 1, 0, 0))

        if noteIdx >= len(notesData) and not gameNotes and endTime == 0:
            endTime = time.perf_counter()
        if endTime != 0 and 1 <= time.perf_counter() - endTime < 2:
            fade.fill((255, 255, 255, 255 * (time.perf_counter() - endTime - 1)))
            shared.songFiles[songName].set_volume(shared.settings['ingameMusicVol'] * (1 - 1 * (time.perf_counter() - endTime - 1)))
        elif endTime != 0 and time.perf_counter() - endTime >= 2:
            shared.songFiles[songName].stop()
            break
        DrawImage(fade, 0, 0, 1, 0, 1)

        # font = pygame.freetype.Font("font/Pretendard-Medium.ttf", 20).render(f'{time.perf_counter() - startTime:.1f}', (255, 255, 255), None)[0]
        # DrawImage(font, -300, 200, 1, 0, 1)
        Update()

    transition = time.perf_counter()
    transition2 = 0
    shared.screen = pygame.Surface((shared.BASE_WIDTH, shared.BASE_HEIGHT))
    fade = pygame.Surface((shared.BASE_WIDTH, shared.BASE_HEIGHT), pygame.SRCALPHA)
    click = False
    if not exitGame:
        if round(scoreText.score) > shared.userData[songName][shared.difficulty]['highScore']:
            shared.userData[songName][shared.difficulty]['highScore'] = round(scoreText.score)
        if scoreText.isFullCombo:
            shared.userData[songName][shared.difficulty]['fullCombo'] = 1
        if scoreText.isPerfect:
            shared.userData[songName][shared.difficulty]['perfect'] = 1
        with open('userdata.json', 'w', encoding='utf-8') as f:
            json.dump(shared.userData, f, ensure_ascii=False, indent=4)
    while True: # result
        if exitGame:
            break
        click = False
        shared.events = pygame.event.get()
        for event in shared.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
        
        DrawImage(images[songName]['Background'], 0, 0, 1, 0, 1)
        DrawImage(images['UI']['ResultBox'], 0, 0, 1, 0, 1)
        DrawImage(images[songName]['Album'], -270, 0, 1, 0, 1)
        font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 60).render(f'{songName}', (255, 255, 255), None)[0]
        DrawImage(font, 0, 390, 1, 0, 1)
        font = pygame.freetype.Font("font/Pretendard-Medium.ttf", 25).render(f'{shared.difficulty.upper()} {shared.songDifficulty[songName][shared.difficulty]}', (255, 255, 255), None)[0]
        DrawImage(font, 0, 310, 1, 0, 1)
        font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 100).render(f'{round(scoreText.score):,}', (255, 255, 255), None)[0]
        DrawImage(font, 295, 135, 1, 0, 1)
        if scoreText.isPerfect:
            font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 30).render('ALL PERFECT', (127, 255, 255), None)[0]
            DrawImage(font, 295, 210, 1, 0, 1)
        elif scoreText.isFullCombo:
            font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 30).render('FULL COMBO', (200, 255, 255), None)[0]
            DrawImage(font, 295, 210, 1, 0, 1)
        font = pygame.freetype.Font("font/Pretendard-Medium.ttf", 36)
        DrawImage(font.render('PERFECT', (255, 255, 255), None)[0], 150, 0, 1, 0, 1)
        DrawImage(font.render(f'{scoreText.perfectCnt:04d}', (255, 255, 255), None)[0], 480, 0, 1, 0, 1)
        DrawImage(font.render('GREAT', (255, 255, 255), None)[0], 129, -60, 1, 0, 1)
        DrawImage(font.render(f'{scoreText.greatCnt:04d}', (255, 255, 255), None)[0], 480, -60, 1, 0, 1)
        DrawImage(font.render('GOOD', (255, 255, 255), None)[0], 124, -120, 1, 0, 1)
        DrawImage(font.render(f'{scoreText.goodCnt:04d}', (255, 255, 255), None)[0], 480, -120, 1, 0, 1)
        DrawImage(font.render('MISS', (255, 255, 255), None)[0], 115, -180, 1, 0, 1)
        DrawImage(font.render(f'{scoreText.missCnt:04d}', (255, 255, 255), None)[0], 480, -180, 1, 0, 1)
        rect = images['UI']['NextBtnOff'].get_rect(center = (860, -250))
        if rect.collidepoint(MousePos()):
            DrawImage(images['UI']['NextBtnOn'], 860, -250, 1, 0, 1)
            if click and transition2 == 0:
                transition2 = time.perf_counter()
        else:
            DrawImage(images['UI']['NextBtnOff'], 860, -250, 1, 0, 1)


        if time.perf_counter() - transition <= 1:
            fade.fill((255, 255, 255, 255 * (1 - (time.perf_counter() - transition))))
            DrawImage(fade, 0, 0, 1, 0, 1)
        if time.perf_counter() - transition2 <= 1.5:
            fade.fill((255, 255, 255, (255 * (time.perf_counter() - transition2)) if time.perf_counter() - transition2 <= 1 else 255))
            DrawImage(fade, 0, 0, 1, 0, 1)
        if 1.5 <= time.perf_counter() - transition2 < 2:
            break

        shared.screen.fill((0, 0, 0))
        Update()

    shared.songFiles[songName].stop()
    shared.scene = 'Lobby'