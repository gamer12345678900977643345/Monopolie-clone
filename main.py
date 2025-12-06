import pygame
import sys
import bord
import json
import random
import player
import UI
import bot_mode
import geluid
pygame.init()

tile_ID = "tileID.json"
with open(tile_ID, 'r') as json_file:
    data = json.load(json_file)
print(data)

def dobbelsteen():
    dobb = random.randint(1,2)
    return dobb
#stat text render
font = pygame.font.SysFont("Tahoma", 30)

def info_screen():
    pygame.draw.rect(bord.Screen.screen, (188, 180, 162), (900, 200,300,240))
    pygame.draw.rect(bord.Screen.screen, (80, 20, 20), (900, 200,300,240),5)

    # naam, prijs, huur, upgrade, eigenaar weergeven
    bord.Screen.screen.blit(font.render(vak["naam"], True, (230,230,230)), (910,220))
    bord.Screen.screen.blit(font.render(f"Prijs: {vak['prijs']}", True, (230,230,230)), (910,260))
    bord.Screen.screen.blit(font.render(f"Huur: {vak['huur']}", True, (230,230,230)), (910,300))
    bord.Screen.screen.blit(font.render(f"Upgrade: {vak['upgrade']}", True, (230,230,230)), (910,340))
    bord.Screen.screen.blit(font.render(f"Eigenaar: {vak['eigenaar']}", True, (230,230,230)), (910,380))
    return
def koop_mechanisme():
    koop_knop = pygame.draw.rect(bord.Screen.screen, (200,200,100), (900, 450,300,60))
    pygame.draw.rect(bord.Screen.screen, (80,20,20), (900, 450,300,60),5)
    bord.Screen.screen.blit(font.render("Koop nu", True, (230,230,230)), (910,460))
    if event.type == pygame.MOUSEBUTTONDOWN:
        if koop_knop.collidepoint(event.pos):
            if(player.speler1.balans > vak["prijs"]):
                vak["eigenaar"] = "Speler1"
                player.speler1.balans -= vak["prijs"]
                player.speler1.eigendom += vak["prijs"]
                print(player.speler1.balans)
            else:
                bord.Screen.screen.blit(font.render("Niet genoeg geld!", True, (230,230,230)), (1200,250))
                print("you broke!")
                pygame.display.flip()
                pygame.time.wait(1000)
    return
geluid.background()
speler_pos_x = 795
speler_pos_y = 130
clock = pygame.time.Clock()
straat = "geel"
running = True
paused = False 
UI.intro() #start scherm
player_mode_choose = True
game_mode = ""
while player_mode_choose == True:
    UI.player_mode()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if UI.pvp_knop.collidepoint(event.pos):
                naam1 = UI.start_settings()
                player.speler1.naam = naam1
                print(f"Speler 1: {naam1}")

                naam2 = UI.start_settings()
                player.speler2.naam = naam2
                print(f"Speler 2: {naam2}")
                game_mode = "pvp"
                player_mode_choose = False
            if UI.bot_knop.collidepoint(event.pos):
                game_mode = "bot"
                player_mode_choose = False
                bot_mode.bot_game()
                print("bot")
while running:
    bord.Screen.screen.fill((75,170,75))#nice groen aub niet veranderen
    speler_pos = (speler_pos_x, speler_pos_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # speler turn dobbelsteen gooien
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check menu knop eerst
            if UI.menu_knop_rect.collidepoint(event.pos):
                paused = not paused  # toggle pauze status
            elif not paused:  # alleen andere knoppen als niet gepauzeerd
                if gooi_knop.collidepoint(event.pos):
                    dobb1=dobbelsteen()
                    dobb2=dobbelsteen()
                    geluid.dobb_eff.play()
                    geluid.move_eff.play()
                    dob_tot = dobb1 + dobb2
                    vakken_opgeschoven = dob_tot #moet spitsen naar x en y en in loop toevoegen
                    #speler beweegt langs gele straat
                    if straat == "geel":
                        speler_pos_y += vakken_opgeschoven*90
                        if speler_pos_y > 580:
                            speler_pos_y = 580
                            straat = "rood"
                    
                    elif straat == "rood":
                        speler_pos_x -= vakken_opgeschoven*80
                        if speler_pos_x < 75:
                            speler_pos_x = 75
                            straat = "groen"
                    
                    elif straat == "groen":
                        speler_pos_y -= vakken_opgeschoven*90
                        if speler_pos_y < 130:
                            speler_pos_y = 130
                            straat = "blauw"
                    
                    elif straat == "blauw":
                        speler_pos_x += vakken_opgeschoven*80
                        if speler_pos_x > 795:
                            speler_pos_x = 795
                            player.speler1.balans += 200
                            straat= "geel"
                    
                    print(speler_pos)
            elif paused:  # check pauze menu knoppen
                if UI.exit_knop_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if UI.continue_knop_rect.collidepoint(event.pos):
                    paused = False

    #tile info check
    for vak in data["rood"]:
        kleur_x = vak["x"]
        if speler_pos_x == kleur_x and straat == "rood":
            # teken het info vak
            info_screen()
            # koop-knop tonen als geen eigenaar
            if vak["eigenaar"] is None:
                koop_mechanisme()
    
    for vak in data["geel"]:
        kleur_y = vak["y"]
        if speler_pos_y == kleur_y and straat == "geel":
            # teken het info vak
            info_screen()
            # koop-knop tonen als geen eigenaar
            if vak["eigenaar"] is None:
                koop_mechanisme()
    
    for vak in data["groen"]:
        kleur_y = vak["y"]
        if speler_pos_y == kleur_y and straat == "groen":
            # teken het info vak
            info_screen()
            # koop-knop tonen als geen eigenaar
            if vak["eigenaar"] is None:
                koop_mechanisme()
    
    for vak in data["blauw"]:
        kleur_x = vak["x"]
        if speler_pos_x == kleur_x and straat == "blauw":
            # teken het info vak
            info_screen()
            # koop-knop tonen als geen eigenaar
            if vak["eigenaar"] is None:
                koop_mechanisme()


    gooi_knop = pygame.draw.rect(bord.Screen.screen, (20,20,20), (950, 100, 100,100))
    
    for i in range(0, 10, 9):#witte hoeken
        pygame.draw.rect(bord.Screen.screen, (255, 255, 255), (80*i+75,130,80,90))
        pygame.draw.rect(bord.Screen.screen, (255, 255, 255), (80*i+75,580,80,90))
        pygame.draw.rect(bord.Screen.screen, (0, 0, 0), (80*i+75,130,80,90), 1)
        pygame.draw.rect(bord.Screen.screen, (0, 0, 0), (80*i+75,580,80,90), 1)
    
    # hieronder print alle vakken en straten op het scherm
    player_0 = pygame.image.load("assets/player0.png").convert_alpha()
    red_tile = pygame.image.load("assets/tile0.png").convert_alpha()
    green_tile = pygame.image.load("assets/tile1.png").convert_alpha()
    blue_tile = pygame.image.load("assets/tile2.png").convert_alpha()
    yellow_tile = pygame.image.load("assets/tile3.png").convert_alpha()
    for i in range(4):
        x = i * red_tile.get_width()
        y = 580
        bord.Screen.screen.blit(red_tile, (x+155,y)) #bottom row (80, 580)
    for i in range(4):
        x = 75 
        y = i *  green_tile.get_height()
        bord.Screen.screen.blit(green_tile, (x,y+220)) #left column (75, 310)
    for i in range(4):
        x = i * blue_tile.get_width()
        y = 130
        bord.Screen.screen.blit(blue_tile, (x+155,y)) #top row (80, 130)
    for i in range(4):
        x = 795 
        y = i *  yellow_tile.get_height()
        bord.Screen.screen.blit(yellow_tile, (x,y+220)) #right column (795, 310)
    # coordinaten regelen##################################################################################################
    #til-ID loop voor red_tile
    for i in range(1,9): #lijn 9 staat de json bestand, kan hiermee vervangd worden
        x = i * blue_tile.get_width()
        y = 130
        red_tile_ID = (x, y)#(80,90)
    
    bord.Screen.screen.blit(player_0, speler_pos)#blit de speler pion
    bord.Screen.screen.blit(font.render(f"Budget: {player.speler1.balans}", True, (230,230,230)), (200, 220))
    bord.Screen.screen.blit(font.render(f"Eigendommen: {player.speler1.eigendom}", True, (230,230,230)), (200,270))
    
    # teken pauze menu als gepauzeerd
    if paused:
        UI.pause_menu()
    else:
        # teken menu knop alleen als niet gepauzeerd
        bord.Screen.screen.blit(UI.menu_knop, (600,0))
    
    pygame.display.flip()
    clock.tick(60)