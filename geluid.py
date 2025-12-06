import pygame
pygame.init()

def background():
    pygame.mixer.music.load("assets/background.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    return


dobb_eff = pygame.mixer.Sound("assets/dobbelsteen_effect.mp3")
pygame.mixer.music.set_volume(1)

move_eff = pygame.mixer.Sound("assets/move_effect.mp3")
pygame.mixer.music.set_volume(1)

get_rent = pygame.mixer.Sound("assets/Sound rent gained.mp3")
pygame.mixer.music.set_volume(5)

pay_rent = pygame.mixer.Sound("assets/rent betalen.mp3")
pygame.mixer.music.set_volume(5)