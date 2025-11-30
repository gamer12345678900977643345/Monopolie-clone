import pygame
import bord
import sys
import player
pygame.init()
rect = pygame.Rect(540,400,200,100) #pos startknop vak
moneypolie = pygame.image.load("assets/moneypolie.png").convert_alpha()
menu_knop = pygame.image.load("assets/menu_icon.png").convert_alpha()
menu_knop_rect = pygame.Rect(600,0,30,30)
font = pygame.font.SysFont("Tahoma", 30)
big_font = pygame.font.SysFont("Tahoma", 100)
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
huidige_speler_nummer = 1
def start_settings():
    global huidige_speler_nummer 
    clock = pygame.time.Clock()
    user_name = ""  # lege string om tekst op te slaan
    # Text input box positie
    input_box = pygame.Rect(460, 400, 600, 50)
    
    blurr = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    pygame.draw.rect(blurr, (255, 255, 255, 200), blurr.get_rect())
    bord.Screen.screen.blit(blurr, (0,0))
    
    # Start knop
    start_rect = pygame.Rect(710, 500, 200, 60)
    waiting = True
    while waiting:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter = klaar
                    if user_name:  # alleen als er iets is ingevuld
                        waiting = False
                elif event.key == pygame.K_BACKSPACE:  # Backspace = verwijder laatste letter
                    user_name = user_name[:-1]
                else:
                    # Voeg letter toe (maximaal 20 karakters)
                    if len(user_name) < 20:
                        user_name += event.unicode  # event.unicode geeft de letter
            
            # Check START knop
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    if user_name:
                        waiting = False
        
        # Herteken scherm
        blurr = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        pygame.draw.rect(blurr, (255, 255, 255, 200), blurr.get_rect())
        bord.Screen.screen.blit(blurr, (0,0))
        
        # Teken instructie
        bord.Screen.screen.blit(font.render("Voer je naam in:", True, (10,10,10)), (460, 350))
        
        # Teken input box
        pygame.draw.rect(bord.Screen.screen, (255, 255, 255), input_box)
        pygame.draw.rect(bord.Screen.screen, (10, 10, 10), input_box, 2)  # border
        
        # Teken de ingevoerde tekst
        text_surface = font.render(user_name, True, (10, 10, 10))
        bord.Screen.screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
        
        # Teken START knop
        pygame.draw.rect(bord.Screen.screen, (255,100,0), start_rect)
        bord.Screen.screen.blit(font.render("START", True, (10,10,10)), (760, 515))
        
        pygame.display.flip()
    
    return user_name if user_name else "Speler1"

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
    bord.Screen.screen.blit(big_font.render("PAUSE", True, (10,10,10)), (600,0))
    
    # teken menu knop bovenop
    bord.Screen.screen.blit(menu_knop, (600,0))
    
    return
pvp_knop = pygame.Rect(800,300,200,100)
bot_knop = pygame.Rect(800,450,200,100)
def player_mode():
    blurr = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    pygame.draw.rect(blurr, (255, 255, 255, 200), blurr.get_rect())
    bord.Screen.screen.blit(blurr, (0,0))
    pygame.draw.rect(bord.Screen.screen, (230,100,100), pvp_knop)
    pygame.draw.rect(bord.Screen.screen, (230,100,100), bot_knop)
    bord.Screen.screen.blit(font.render("PVP", True, (10,10,10)), (850,350))
    bord.Screen.screen.blit(font.render("bot", True, (10,10,10)), (850,500))
    pygame.display.flip()
    return