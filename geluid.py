import pygame
pygame.init()

def background():
    pygame.mixer.music.load("assets/background.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    return

def dobbelsteen_effect():
    pygame.mixer.music.load("assets/dobbelsteen_effect.mp3")
    pygame.mixer.music.set_volume(0.5)
    return

def move_effect():
    pygame.mixer.music.load("assets/move_effect.mp3")
    pygame.mixer.music.set_volume(0.5)
    return