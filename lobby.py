import pygame
import time
import json
import shared
from images import *
from update import *
from mouse import *

def DrawImage2D(image, layer, x, y):
    shared.layers.append((image, layer, x - image.get_width() / 2 + 960, 540 - y - image.get_height() / 2))

def DrawPolygon2D(points, color, surface):
    newPoints = []
    for x, y in points:
        newPoints.append((x + surface.get_width() / 2, surface.get_height() / 2 - y))
    pygame.draw.polygon(surface, color, newPoints)

transition2 = 0

class SongSection:
    def __init__(self):
        import pygame.freetype
        self.x = -200
        self.onCursor = None
        self.titleFont = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 60)
        self.highScoreFont = pygame.freetype.Font("font/Pretendard-Medium.ttf", 32)
        self.highScoreVFont = pygame.freetype.Font("font/Pretendard-Medium.ttf", 48)
        self.infoFont = pygame.freetype.Font("font/Pretendard-Medium.ttf", 24)
        self.difficultyFont = pygame.freetype.Font("font/Pretendard-Medium.ttf", 20)
        self.difficultyVFont = pygame.freetype.Font("font/Pretendard-Medium.ttf", 48)

    def Update(self):
        global transition2
        self.x += (0 - self.x) * 0.2
        click = False
        if transition2 == 0:
            for event in shared.events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
        mousePos = MousePos()
        songName = shared.songList[shared.curSongIdx]
        DrawImage2D(images['UI']['SongSection'], 0, -448.375 + self.x, 0)
        DrawImage2D(images[songName]['Album'], 0, -262.5 + self.x, -4)
        DrawImage2D(self.titleFont.render(songName, (255, 255, 255), None)[0], 0, -446.25 + self.x, 322.5)
        DrawImage2D(self.highScoreFont.render('HIGH SCORE', (179, 179, 179), None)[0], 0, -710 + self.x, 160)
        DrawImage2D(self.highScoreVFont.render(f'{shared.userData[songName][shared.difficulty]['highScore']:,}', (255, 255, 255), None)[0], 0, -710 + self.x, 115)
        if shared.userData[songName][shared.difficulty]['perfect']:
            DrawImage2D(images['UI']['BadgePerfect'], 0, -840 + self.x, 119)
            DrawImage2D(images['UI']['BadgePerfect'], 0, -580 + self.x, 119)
        elif shared.userData[songName][shared.difficulty]['fullCombo']:
            DrawImage2D(images['UI']['BadgeFullCombo'], 0, -840 + self.x, 119)
            DrawImage2D(images['UI']['BadgeFullCombo'], 0, -580 + self.x, 119)
        DrawImage2D(self.infoFont.render('Music by', (179, 179, 179), None)[0], 0, -710 + self.x, -75)
        DrawImage2D(self.infoFont.render(shared.songInfo[songName]['Music by'], (179, 179, 179), None)[0], 0, -710 + self.x, -105)
        DrawImage2D(self.infoFont.render('Level by', (179, 179, 179), None)[0], 0, -710 + self.x, -150)
        DrawImage2D(self.infoFont.render(shared.songInfo[songName]['Level by'], (179, 179, 179), None)[0], 0, -710 + self.x, -180)
        if (-710 + self.x - mousePos[0])**2 + (20 - mousePos[1])**2 < 2500:
            DrawImage2D(images['UI']['PlayBtnOn'], 0, -710 + self.x, 20)
            if click and shared.songDifficulty[songName][shared.difficulty] != 0:
                transition2 = time.perf_counter()
        else:
            DrawImage2D(images['UI']['PlayBtnOff'], 0, -710 + self.x, 20)
        
        rect = images['UI']['DifficultyBtnOff'].get_rect(center = (-607.5 + self.x, -327)).inflate(-45,0)
        if rect.collidepoint(mousePos):
            self.onCursor = 'EasyBtn'
            if click:
                shared.difficulty = 'Easy'
        rect = images['UI']['DifficultyBtnOff'].get_rect(center = (-427.5 + self.x, -327)).inflate(-45,0)
        if rect.collidepoint(mousePos):
            self.onCursor = 'NormalBtn'
            if click:
                shared.difficulty = 'Normal'
        rect = images['UI']['DifficultyBtnOff'].get_rect(center = (-247.5 + self.x, -327)).inflate(-45,0)
        if rect.collidepoint(mousePos):
            self.onCursor = 'HardBtn'
            if click:
                shared.difficulty = 'Hard'
        
        if self.onCursor == 'EasyBtn' or shared.difficulty == 'Easy':
            DrawImage2D(images['UI']['DifficultyBtnOn'], 0, -607.5 + self.x, -327)
        else:
            DrawImage2D(images['UI']['DifficultyBtnOff'], 0, -607.5 + self.x, -327)
        DrawImage2D(self.difficultyFont.render('EASY', (179, 179, 179), None)[0], 0, -607.5 + self.x, -300)
        DrawImage2D(self.difficultyVFont.render(f'{shared.songDifficulty[songName]['Easy']}', (179, 179, 179), None)[0], 0, -607.5 + self.x, -335)

        if self.onCursor == 'NormalBtn' or shared.difficulty == 'Normal':
            DrawImage2D(images['UI']['DifficultyBtnOn'], 0, -427.5 + self.x, -327)
        else:
            DrawImage2D(images['UI']['DifficultyBtnOff'], 0, -427.5 + self.x, -327)
        DrawImage2D(self.difficultyFont.render('NORMAL', (179, 179, 179), None)[0], 0, -427.5 + self.x, -300)
        DrawImage2D(self.difficultyVFont.render(f'{shared.songDifficulty[songName]['Normal']}', (179, 179, 179), None)[0], 0, -427.5 + self.x, -335)

        if self.onCursor == 'HardBtn' or shared.difficulty == 'Hard':
            DrawImage2D(images['UI']['DifficultyBtnOn'], 0, -247.5 + self.x, -327)
        else:
            DrawImage2D(images['UI']['DifficultyBtnOff'], 0, -247.5 + self.x, -327)
        DrawImage2D(self.difficultyFont.render('HARD', (179, 179, 179), None)[0], 0, -247.5 + self.x, -300)
        DrawImage2D(self.difficultyVFont.render(f'{shared.songDifficulty[songName]['Hard']}', (179, 179, 179), None)[0], 0, -247.5 + self.x, -335)

class SelectionBox:
    scroll = 0
    pos = ((225, 450), (150, 300), (75, 150), (0, 0), (75, -150), (150, -300), (225, -450))
    def __init__(self, posIdx, songName): # posIdx 1부터 시작
        import pygame.freetype
        self.posIdx = posIdx
        self.surface = images[songName]['SelectionBox'].copy()
        font = pygame.freetype.Font("font/Pretendard-Medium.ttf", 32).render(songName, (255, 255, 255), None)[0]
        self.surface.blit(font, (50, self.surface.get_height() / 2 - font.get_height() / 2))
        self.alpha = 255

        relative = self.posIdx - SelectionBox.scroll
        if relative < 0:
            relative = 0
        if relative > 6:
            relative = 6
        if abs(relative - 3) > 2:
            self.alpha = 0
            self.surface.set_alpha(0)

        self.x = 540 + SelectionBox.pos[relative][0]
        self.y = 0 + SelectionBox.pos[relative][1]

    def Update(self):
        relative = self.posIdx - SelectionBox.scroll
        if relative < 0:
            relative = 0
        if relative > 6:
            relative = 6

        self.x += (540 + SelectionBox.pos[relative][0] - self.x) * 0.2
        self.y += (0 + SelectionBox.pos[relative][1] - self.y) * 0.2
        
        if abs(relative - 3) > 2:
            self.alpha += (0 - self.alpha) * 0.2
        else:
            self.alpha += (255 - self.alpha) * 0.2

        self.surface.set_alpha(self.alpha)
        DrawImage2D(self.surface, 0, self.x, self.y)

class Slider:
    def __init__(self, surface, x, y, key):
        self.surface = surface
        self.x = x
        self.y = y
        self.key = key
        if key == 'offset':
            self.maxi = 0.3
            self.mini = -0.3
        elif key == 'noteSpeed':
            self.maxi = 0.6
            self.mini = 1.5
        else:
            self.maxi = 1
            self.mini = 0
        self.drag = False
    def Update(self):
        rect = pygame.Rect(self.x - 250, self.y - 15, 500, 30)
        for event in shared.events:
            if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(MousePos()):
                self.drag = True
            elif self.drag and event.type == pygame.MOUSEBUTTONUP:
                self.drag = False
                shared.userData['Settings'] = shared.settings
                with open('userdata.json', 'w', encoding='utf-8') as f:
                    json.dump(shared.userData, f, ensure_ascii=False, indent=4)
        if self.drag:
            progress = (MousePos()[0] - (self.x - 250)) / 500
            if progress < 0:
                progress = 0
            if progress > 1:
                progress = 1
            if self.key == 'offset':
                rdigit = 3
            elif self.key == 'noteSpeed':
                rdigit = 1
            else:
                rdigit = 2
            shared.settings[self.key] = round((self.maxi - self.mini) * progress + self.mini, rdigit)
        progress = (shared.settings[self.key] - self.mini) / (self.maxi - self.mini)
        p1 = (self.x - 250, self.y + 7)
        p2 = (self.x + 250, self.y + 7)
        p3 = (self.x - 250, self.y - 7)
        p4 = (self.x + 250, self.y - 7)
        DrawPolygon2D((p1, p2, p4, p3), (127, 127, 127), self.surface)
        p1 = (self.x - 250 + 500 * progress - 10, self.y + 20)
        p2 = (self.x - 250 + 500 * progress + 10, self.y + 20)
        p3 = (self.x - 250 + 500 * progress - 10, self.y - 20)
        p4 = (self.x - 250 + 500 * progress + 10, self.y - 20)
        DrawPolygon2D((p1, p2, p4, p3), (180, 180, 180), self.surface)

class SettingsBox:
    def __init__(self):
        self.surface = pygame.Surface((images['UI']['SettingsBox'].get_width(), images['UI']['SettingsBox'].get_height()), pygame.SRCALPHA)
        self.on = False
        self.sliders = []
        self.sliders.append(Slider(self.surface, -350, 160, 'lobbyMusicVol'))
        self.sliders.append(Slider(self.surface, -350, 20, 'lobbySfxVol'))
        self.sliders.append(Slider(self.surface, -350, -120, 'ingameMusicVol'))
        self.sliders.append(Slider(self.surface, -350, -260, 'ingameSfxVol'))
        self.sliders.append(Slider(self.surface, 350, 90, 'offset'))
        self.sliders.append(Slider(self.surface, 350, -190, 'noteSpeed'))
    def Update(self):
        import pygame.freetype
        self.surface.fill((0, 0, 0, 0))
        for slider in self.sliders:
            slider.Update()
        DrawImage2D(images['UI']['SettingsBox'], 0, 0, 0)
        DrawImage2D(self.surface, 0, 0, 0)
        font = pygame.freetype.Font("font/Pretendard-SemiBold.ttf", 60)
        DrawImage2D(font.render('SETTINGS', (255, 255, 255), None)[0], 0, 0, 330)
        font = pygame.freetype.Font("font/Pretendard-Medium.ttf", 30)
        DrawImage2D(font.render('로비 배경음악 볼륨', (255, 255, 255), None)[0], 0, -350, 210)
        DrawImage2D(font.render(f'{round(shared.settings['lobbyMusicVol'] * 100)}', (255, 255, 255), None)[0], 0, -50, 160)
        DrawImage2D(font.render('로비 효과음 볼륨', (255, 255, 255), None)[0], 0, -350, 70)
        DrawImage2D(font.render(f'{round(shared.settings['lobbySfxVol'] * 100)}', (255, 255, 255), None)[0], 0, -50, 20)
        DrawImage2D(font.render('게임 배경음악 볼륨', (255, 255, 255), None)[0], 0, -350, -70)
        DrawImage2D(font.render(f'{round(shared.settings['ingameMusicVol'] * 100)}', (255, 255, 255), None)[0], 0, -50, -120)
        DrawImage2D(font.render('게임 효과음 볼륨', (255, 255, 255), None)[0], 0, -350, -210)
        DrawImage2D(font.render(f'{round(shared.settings['ingameSfxVol'] * 100)}', (255, 255, 255), None)[0], 0, -50, -260)
        DrawImage2D(font.render('오프셋', (255, 255, 255), None)[0], 0, 350, 140)
        DrawImage2D(font.render(f'{round(shared.settings['offset'] * 1000)}', (255, 255, 255), None)[0], 0, 650, 90)
        DrawImage2D(font.render('노트 속도', (255, 255, 255), None)[0], 0, 350, -140)
        DrawImage2D(font.render(f'{16 - round(shared.settings['noteSpeed'] * 10)}', (255, 255, 255), None)[0], 0, 650, -190)
        font = pygame.freetype.Font("font/Pretendard-Medium.ttf", 20)
        DrawImage2D(font.render('노트가 음악보다 빠르다면 오프셋을 올려주세요.', (255, 255, 255), None)[0], 0, 350, 40)
        DrawImage2D(font.render('노트가 음악보다 느리다면 오프셋을 내려주세요.', (255, 255, 255), None)[0], 0, 350, 10)

def Lobby():
    global transition2
    transition2 = 0
    prevPressedKeys = pygame.key.get_pressed()
    songName = shared.songList[shared.curSongIdx]
    songSection = SongSection()
    selectionBoxes = []
    offset = shared.curSongIdx
    SelectionBox.scroll = 0
    for i in range(5):
        selectionBoxes.append(SelectionBox(i + 1, shared.songList[(i + offset - 2) % len(shared.songList)]))
    settingsBox = SettingsBox()
    songVol = 1
    songChanged = True
    songStartTime = 0
    fade = pygame.Surface((shared.BASE_WIDTH, shared.BASE_HEIGHT), pygame.SRCALPHA)
    transition = time.perf_counter()

    while shared.scene == 'Lobby':
        click = False
        shared.events = pygame.event.get()
        for event in shared.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if transition2 == 0 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        wheelScroll = 0
        for event in shared.events:
            if event.type == pygame.MOUSEWHEEL:
                wheelScroll = event.y
        if transition2 == 0:
            if pygame.key.get_pressed()[pygame.K_UP] and not prevPressedKeys[pygame.K_UP] or wheelScroll == 1:
                fadingBox = next((box for box in selectionBoxes if box.posIdx == SelectionBox.scroll), None)
                if fadingBox == None or fadingBox.alpha <= 10:
                    selectionBoxes.append(SelectionBox(SelectionBox.scroll, shared.songList[(offset + SelectionBox.scroll - 3) % len(shared.songList)]))
                SelectionBox.scroll -= 1
                songSection.x = -200
                songChanged = True
            elif pygame.key.get_pressed()[pygame.K_DOWN] and not prevPressedKeys[pygame.K_DOWN] or wheelScroll == -1:
                fadingBox = next((box for box in selectionBoxes if box.posIdx == SelectionBox.scroll + 6), None)
                if fadingBox == None or fadingBox.alpha <= 10:
                    selectionBoxes.append(SelectionBox(SelectionBox.scroll + 6, shared.songList[(offset + SelectionBox.scroll + 3) % len(shared.songList)]))
                SelectionBox.scroll += 1
                songSection.x = -200
                songChanged = True
            shared.curSongIdx = (offset + SelectionBox.scroll) % len(shared.songList)
        
        if songChanged:
            shared.songFiles[songName + ' Preview'].stop()
        
        songName = shared.songList[shared.curSongIdx]
        DrawImage2D(images[songName]['Background'], 10, 0, 0)

        if songChanged:
            songChanged = False
            songVol = 0
            shared.songFiles[songName + ' Preview'].play()
            songStartTime = time.perf_counter()

        if time.perf_counter() - songStartTime < shared.songFiles[songName + ' Preview'].get_length() - 2:
            songVol += 1 / 50
        else:
            songVol -= 1 / 50
        if songVol > 1:
            songVol = 1
        if songVol < 0:
            songVol = 0
            songChanged = True
        shared.songFiles[songName + ' Preview'].set_volume(songVol * shared.settings['lobbyMusicVol'])

        songSection.onCursor = None
        songSection.Update()
        for box in selectionBoxes:
            box.Update()
        selectionBoxes = [box for box in selectionBoxes if box.alpha > 10]

        rect = images['UI']['SettingsBox'].get_rect(center = (0, 0))
        if not rect.collidepoint(MousePos()) and click:
            settingsBox.on = False
        rect = images['UI']['SettingsBtnOff'].get_rect(center = (870, 502.5))
        if rect.collidepoint(MousePos()) or settingsBox.on:
            DrawImage2D(images['UI']['SettingsBtnOn'], 0, 870, 502.5)
            if click:
                settingsBox.on = True
        else:
            DrawImage2D(images['UI']['SettingsBtnOff'], 0, 870, 502.5)
        if settingsBox.on:
            settingsBox.Update()

        prevPressedKeys = pygame.key.get_pressed()

        if time.perf_counter() - transition <= 1:
            fade.fill((255, 255, 255, 255 * (1 - (time.perf_counter() - transition))))
            DrawImage2D(fade, 0, 0, 0)
        if time.perf_counter() - transition2 <= 1.5:
            fade.fill((255, 255, 255, (255 * (time.perf_counter() - transition2)) if time.perf_counter() - transition2 <= 1 else 255))
            DrawImage2D(fade, 0, 0, 0)
        if 1.5 <= time.perf_counter() - transition2 < 2:
            shared.scene = 'Ingame'

        Update()

    shared.songFiles[songName + ' Preview'].stop()