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

curSongIdx = 0
difficulty = 'Easy'
songList = ['염라', '잔혹한 천사의 테제', 'PPPP', 'danser', 'Flower Rocket']
songFiles = {
    'PPPP' : pygame.mixer.Sound('songs/PPPP.mp3'),
    'PPPP Preview' : pygame.mixer.Sound('songs/PPPP_Preview.mp3'),
    '잔혹한 천사의 테제' : pygame.mixer.Sound('songs/Janhok.mp3'),
    '잔혹한 천사의 테제 Preview' : pygame.mixer.Sound('songs/Janhok_Preview.mp3'),
    'Flower Rocket' : pygame.mixer.Sound('songs/Flower.mp3'),
    'Flower Rocket Preview' : pygame.mixer.Sound('songs/Flower_Preview.mp3'),
    '염라' : pygame.mixer.Sound('songs/Karma.mp3'),
    '염라 Preview' : pygame.mixer.Sound('songs/Karma_Preview.mp3'),
    'danser' : pygame.mixer.Sound('songs/danser.mp3'),
    'danser Preview' : pygame.mixer.Sound('songs/danser_Preview.mp3'),
}
songInfo = {
    'PPPP' : {'Music by' : 'TAK', 'Level by' : 'HeartbeatUdon'},
    '잔혹한 천사의 테제' : {'Music by' : 'Yoko Takahashi', 'Level by' : 'MilQShake'},
    'Flower Rocket' : {'Music by' : 'Plum', 'Level by' : '도르돌'},
    '염라' : {'Music by' : '달의하루', 'Level by' : 'CTPR'},
    'danser' : {'Music by' : 'gladde paling', 'Level by' : 'Moz'},
}
songDifficulty = {
    'PPPP' : {'Easy' : 0, 'Normal' : 0, 'Hard' : 19},
    '잔혹한 천사의 테제' : {'Easy' : 0, 'Normal' : 11, 'Hard' : 17},
    'Flower Rocket' : {'Easy' : 5, 'Normal' : 12, 'Hard' : 99},
    '염라' : {'Easy' : 5, 'Normal' : 10, 'Hard' : 15},
    'danser' : {'Easy' : 0, 'Normal' : 0, 'Hard' : 30},
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
with open("charts/Karma_Normal.json", "r", encoding="utf-8") as f: charts['염라']['Normal'] = json.load(f)
with open("charts/Karma_Hard.json", "r", encoding="utf-8") as f: charts['염라']['Hard'] = json.load(f)
with open("charts/danser_Hard.json", "r", encoding="utf-8") as f: charts['danser']['Hard'] = json.load(f)

sfxFiles = {
    'Hit' : pygame.mixer.Sound('sfx/Hit.mp3'),
    'Flick' : pygame.mixer.Sound('sfx/Flick.mp3'),
    'Scroll' : pygame.mixer.Sound('sfx/Scroll.mp3'),
    'Start' : pygame.mixer.Sound('sfx/Start.mp3'),
    'Button' : pygame.mixer.Sound('sfx/Button.mp3'),
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
settings = userData['Settings']
