import pygame
import bord
import sys
pygame.init()
rect = pygame.Rect(540,400,200,100) #pos startknop vak
moneypolie = pygame.image.load("assets/moneypolie.png").convert_alpha()
menu_knop = pygame.image.load("assets/menu_icon.png").convert_alpha()
menu_knop_rect = pygame.Rect(600,0,30,30)
font = pygame.font.SysFont("Tahoma", 30)
def intro():
    blurr = pygame.Surface((int(bord.Screen.breedte), int(bord.Screen.hoogte)), pygame.SRCALPHA)
    pygame.draw.rect(blurr, (255, 255, 255, 200), blurr.get_rect())
    bord.Screen.screen.blit(blurr, (0,0))#tot hier is de achtergrond
    pygame.draw.rect(bord.Screen.screen, (255,100,0), rect)#start knop vak
    bord.Screen.screen.blit(moneypolie, (350,10))#blit de logo
    bord.Screen.screen.blit(font.render("START", True, (10,10,10)),(600,430)) #blit de start text   
    pygame.display.flip()
    waiting = True
    while waiting == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    bord.Screen.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    waiting = False    
    pygame.display.flip()
    return

def start_settings():
    blurr = pygame.Surface((int(bord.Screen.breedte), int(bord.Screen.hoogte)), pygame.SRCALPHA)
    pygame.draw.rect(blurr, (255, 255, 255, 200), blurr.get_rect())
    bord.Screen.screen.blit(blurr, (0,0)) #tot hier achtergrond
    
    
    return

exit_knop_rect = pygame.Rect(150,500,160,100)
continue_knop_rect= pygame.Rect(150,700,160,100)

def pause_menu():
    # teken blur en menu overlay
    blurr = pygame.Surface((1920,1080), pygame.SRCALPHA)
    pygame.draw.rect(blurr, (255, 255, 255, 210), blurr.get_rect())
    bord.Screen.screen.blit(blurr, (0,0)) #tot hier achtergrond
    
    # teken knoppen
    pygame.draw.rect(bord.Screen.screen, (230,100,100), exit_knop_rect)
    pygame.draw.rect(bord.Screen.screen, (230,100,100), continue_knop_rect)
    bord.Screen.screen.blit(font.render("EXIT", True,(230,230,230)), (185,560))
    bord.Screen.screen.blit(font.render("CONTINUE", True,(230,230,230)), (155,760))
    
    # teken menu knop bovenop
    bord.Screen.screen.blit(menu_knop, (600,0))
    
    return