import pygame

images = {
    'UI' : {
        'Title' : pygame.image.load('images/Title.png').convert_alpha(),
        'SongSection' : pygame.image.load('images/SongSection.png').convert_alpha(),
        'DifficultyBtnOn' : pygame.image.load('images/DifficultyBtnOn.png').convert_alpha(),
        'DifficultyBtnOff' : pygame.image.load('images/DifficultyBtnOff.png').convert_alpha(),
        'PlayBtnOn' : pygame.image.load('images/PlayBtnOn.png').convert_alpha(),
        'PlayBtnOff' : pygame.image.load('images/PlayBtnOff.png').convert_alpha(),
        'SettingsBtnOn' : pygame.image.load('images/SettingsBtnOn.png').convert_alpha(),
        'SettingsBtnOff' : pygame.image.load('images/SettingsBtnOff.png').convert_alpha(),
        'ResultBox' : pygame.image.load('images/ResultBox.png').convert_alpha(),
        'NextBtnOn' : pygame.image.load('images/NextBtnOn.png').convert_alpha(),
        'NextBtnOff' : pygame.image.load('images/NextBtnOff.png').convert_alpha(),
        'BadgeFullCombo' : pygame.image.load('images/BadgeFullCombo.png').convert_alpha(),
        'BadgePerfect' : pygame.image.load('images/BadgePerfect.png').convert_alpha(),
        'SettingsBox' : pygame.image.load('images/SettingsBox.png').convert_alpha(),
        'Tutorial' : pygame.image.load('images/Tutorial.png').convert_alpha(),
    },
    'PPPP' : {
        'Album' : pygame.image.load('images/PPPP_Album.png').convert_alpha(),
        'Background' : pygame.image.load('images/PPPP_Background.png').convert(),
        'SelectionBox' : pygame.image.load('images/PPPP_SelectionBox.png').convert_alpha(),
        'BGA' : 'bga/PPPP_BGA.mp4'
    },
    '잔혹한 천사의 테제' : {
        'Album' : pygame.image.load('images/Janhok_Album.png').convert_alpha(),
        'Background' : pygame.image.load('images/Janhok_Background.png').convert(),
        'SelectionBox' : pygame.image.load('images/Janhok_SelectionBox.png').convert_alpha(),
        'BGA' : 'bga/Janhok_BGA.mp4'
    },
    'Flower Rocket' : {
        'Album' : pygame.image.load('images/Flower_Album.png').convert_alpha(),
        'Background' : pygame.image.load('images/Flower_Background.png').convert(),
        'SelectionBox' : pygame.image.load('images/Flower_SelectionBox.png').convert_alpha(),
        'BGA' : 'bga/Flower_BGA.mp4'
    },
    '염라' : {
        'Album' : pygame.image.load('images/Karma_Album.png').convert_alpha(),
        'Background' : pygame.image.load('images/Karma_Background.png').convert(),
        'SelectionBox' : pygame.image.load('images/Karma_SelectionBox.png').convert_alpha(),
        'BGA' : 'bga/Karma_BGA.mp4',
    },
    'danser' : {
        'Album' : pygame.image.load('images/danser_Album.png').convert_alpha(),
        'Background' : pygame.image.load('images/danser_Background.png').convert(),
        'SelectionBox' : pygame.image.load('images/danser_SelectionBox.png').convert_alpha(),
        'BGA' : 'bga/danser_BGA.mp4',
    },
}

colors = {
    '염라' : {
        'PlayArea' : (50, 50, 50, 127),
        'CheckLine' : (200, 200, 200),
        'TapNote' : (255, 200, 50),
        'HoldNote' : (255, 200, 50, 127),
        'FlickNote' : (255, 250, 150),
    },
    '잔혹한 천사의 테제' : {
        'PlayArea' : (100, 100, 100, 127),
        'CheckLine' : (200, 200, 200),
        'TapNote' : (200, 150, 255),
        'HoldNote' : (200, 150, 255, 127),
        'FlickNote' : (150, 255, 150),
    },
    'Flower Rocket' : {
        'PlayArea' : (100, 100, 100, 127),
        'CheckLine' : (200, 200, 200),
        'TapNote' : (255, 240, 180),
        'HoldNote' : (255, 240, 180, 127),
        'FlickNote' : (180, 240, 255),
    },
    'PPPP' : {
        'PlayArea' : (100, 100, 100, 127),
        'CheckLine' : (200, 200, 200),
        'TapNote' : (180, 240, 255),
        'HoldNote' : (180, 240, 255, 127),
        'FlickNote' : (255, 200, 180),
    },
    'danser' : {
        'PlayArea' : (100, 100, 100, 127),
        'CheckLine' : (200, 200, 200),
        'TapNote' : (180, 240, 255),
        'HoldNote' : (180, 240, 255, 127),
        'FlickNote' : (255, 240, 180),
    },
}