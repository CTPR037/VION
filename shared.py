import pygame
import json
from screenScaling import *

screen = None
gameScreen = None
BASE_WIDTH, BASE_HEIGHT = 1920, 1080 # 1920 1080
GAME_WIDTH, GAME_HEIGHT = 1280, 720
letterbox = None
scene = None

layers = [] # (Surface, layeridx, x, y)

events = []

curSongIdx = 4
difficulty = 'Hard'
songList = ['PPPP', 'IRIS OUT', '잔혹한 천사의 테제', 'Flower Rocket', '염라']
songFiles = {
    'PPPP' : pygame.mixer.Sound('songs/PPPP.mp3'),
    'PPPP Preview' : pygame.mixer.Sound('songs/PPPP_Preview.mp3'),
    'IRIS OUT' : pygame.mixer.Sound('songs/IRIS OUT.mp3'),
    'IRIS OUT Preview' : pygame.mixer.Sound('songs/IRIS OUT_Preview.mp3'),
    '잔혹한 천사의 테제' : pygame.mixer.Sound('songs/Janhok.mp3'),
    '잔혹한 천사의 테제 Preview' : pygame.mixer.Sound('songs/Janhok_Preview.mp3'),
    'Flower Rocket' : pygame.mixer.Sound('songs/Flower Rocket.mp3'),
    'Flower Rocket Preview' : pygame.mixer.Sound('songs/Flower Rocket_Preview.mp3'),
    '염라' : pygame.mixer.Sound('songs/Karma.mp3'),
    '염라 Preview' : pygame.mixer.Sound('songs/Karma_Preview.mp3'),
}
songInfo = {
    'PPPP' : {'Music by' : 'TAK', 'Level by' : '박동우'},
    'IRIS OUT' : {'Music by' : 'Kenshi Yonezu', 'Level by' : 'Moz'},
    '잔혹한 천사의 테제' : {'Music by' : 'Yoko Takahashi', 'Level by' : '밀퀴셰이크'},
    'Flower Rocket' : {'Music by' : 'Plum', 'Level by' : '현이'},
    '염라' : {'Music by' : '달의하루', 'Level by' : 'CTPR'},
}
songDifficulty = {
    'PPPP' : {'Easy' : 5, 'Normal' : 10, 'Hard' : 15},
    'IRIS OUT' : {'Easy' : 5, 'Normal' : 10, 'Hard' : 15},
    '잔혹한 천사의 테제' : {'Easy' : 5, 'Normal' : 10, 'Hard' : 15},
    'Flower Rocket' : {'Easy' : 5, 'Normal' : 10, 'Hard' : 15},
    '염라' : {'Easy' : 5, 'Normal' : 10, 'Hard' : 15},
}

charts = {}
for song in songList:
    charts[song] = {}
with open("charts/PPPP_Hard.json", "r", encoding="utf-8") as f: charts['PPPP']['Hard'] = json.load(f)
with open("charts/Janhok_Normal.json", "r", encoding="utf-8") as f: charts['잔혹한 천사의 테제']['Normal'] = json.load(f)
with open("charts/Janhok_Hard.json", "r", encoding="utf-8") as f: charts['잔혹한 천사의 테제']['Hard'] = json.load(f)
with open("charts/Flower_Easy.json", "r", encoding="utf-8") as f: charts['Flower Rocket']['Easy'] = json.load(f)
with open("charts/Flower_Normal.json", "r", encoding="utf-8") as f: charts['Flower Rocket']['Normal'] = json.load(f)
with open("charts/Flower_Hard.json", "r", encoding="utf-8") as f: charts['Flower Rocket']['Hard'] = json.load(f)
with open("charts/Karma_Easy.json", "r", encoding="utf-8") as f: charts['염라']['Easy'] = json.load(f)
with open("charts/Karma_Hard.json", "r", encoding="utf-8") as f: charts['염라']['Hard'] = json.load(f)

sfxFiles = {
    'Hit' : pygame.mixer.Sound('sfx/Hit.mp3'),
    'Flick' : pygame.mixer.Sound('sfx/Flick.mp3'),
}

class Settings:
    def __init__(self, data):
        self.lobbyMusicVol = data["lobbyMusicVol"]
        self.lobbySfxVol = data["lobbySfxVol"]
        self.ingameMusicVol = data['ingameMusicVol']
        self.ingameSfxVol = data['ingameSfxVol']
        self.offset = data['offset'] # s -0.2
        self.noteSpeed = data['noteSpeed'] # duration (s) minimum 0.5

with open("userData.json", "r", encoding="utf-8") as f:
    userData = json.load(f)
settings = Settings(userData['Settings'])
