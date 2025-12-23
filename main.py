import pygame
import sys
import bord
import json
import random
import player
import UI
import bot_mode
import geluid
import logic
import pvp_mode
pygame.init()

tile_ID = "tileID.json"
with open(tile_ID, 'r') as json_file:
    data = json.load(json_file)
print(data)


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
dobbelsteen_choose = True
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
                pvp_mode.pvp_game()
            if UI.bot_knop.collidepoint(event.pos):
                game_mode = "bot"
                player_mode_choose = False
                bot_mode.bot_game()
                print("bot")
