import pygame
import sys
import bord
import json
import random
pygame.init()

bord.Screen.screen

tile_ID = "tileID.json"
with open(tile_ID, 'r') as json_file:
    data = json.load(json_file)
print(data)

def dobbelsteen():
    dobb = random.randint(1,4)
    return dobb
#stat text render
font = pygame.font.SysFont("Tahoma", 30)


speler_pos_x = 795
speler_pos_y = 130
clock = pygame.time.Clock()
straat = "geel"
running = True
while running:
    bord.Screen.screen.fill((75,170,75))#nice groen aub niet veranderen
    speler_pos = (speler_pos_x, speler_pos_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # speler turn dobbelsteen gooien
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gooi_knop.collidepoint(event.pos):
                dobb1=dobbelsteen()
                dobb2=dobbelsteen()
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
                        straat= "geel"


                print(speler_pos)
    #tile info check
    for vak in data["rood"]:
        kleur_x = vak["x"]
        kleur_naam = vak["naam"]
        kleur_prijs = str(vak["prijs"])
        kleur_huur = str(vak["huur"])
        kleur_upgrade = str(vak["upgrade"])
        kleur_eigenaar = vak["eigenaar"]
        stat_naam = font.render(kleur_naam, True, (230,230,230))
        stat_prijs = font.render(f"Prijs: {kleur_prijs}", True, (230,230,230))
        stat_huur = font.render(f"Huur: {kleur_huur}", True, (230,230,230))
        stat_upgrade = font.render(f"Upgrade: {kleur_upgrade}", True, (230,230,230))
        stat_eigenaar = font.render(f"Eigenaar: {kleur_eigenaar}", True, (230,230,230))
        koop_knop = font.render("Koop nu", True, (230,230,230))
        if speler_pos_x == kleur_x and straat == "rood":
            pygame.draw.rect(bord.Screen.screen, (188, 180, 162), (900, 200,300,240))
            pygame.draw.rect(bord.Screen.screen, (80, 20, 20), (900, 200,300,240),5)
            bord.Screen.screen.blit(stat_naam,(910,220))
            bord.Screen.screen.blit(stat_prijs, (910,260))
            bord.Screen.screen.blit(stat_huur, (910,300))
            bord.Screen.screen.blit(stat_upgrade, (910,340))
            bord.Screen.screen.blit(stat_eigenaar, (910,380))
            if kleur_eigenaar == None:
                pygame.draw.rect(bord.Screen.screen, (200,200,100), (900, 450,300,60))
                pygame.draw.rect(bord.Screen.screen, (80,20,20), (900, 450,300,60),5)
                bord.Screen.screen.blit(koop_knop, (910, 460))



    gooi_knop = pygame.draw.rect(bord.Screen.screen, (20,20,20), (950, 100, 100,100))

    for i in range(0, 10, 9):#witte hoeken
        pygame.draw.rect(bord.Screen.screen, (255, 255, 255), (80*i+75,130,80,90))
        pygame.draw.rect(bord.Screen.screen, (255, 255, 255), (80*i+75,580,80,90))
    
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
        #een soort tile-ID voor elk gegenereerd kopie van red_tile
        #als speler land op vak met (x,y) coördinaat dan toon vak info/stats (zoals koop prijs, huurprijs, upgrade prijs)
        #tile-ID kan met (x, y, w, h): (x = i * red_tile.get_width(), y= 580, red_tile.get_witdt(), red_tile.get_height())
        #kan de tile tekenen in een- for i in range(1,5): - loop
        #dan in if loops de game logica schrijven
        #ik hoef de rectagle niet te tekenen, gewoon speler naar coordinaten sturen en in game logica if regels te gerbuiken
        #om stats te tonen, de pion van de speler moet ook 80x90 zijn zodat de origens overeenkomen
        # for loops gebruiken om tile-ID te generen 
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
        #print(red_tile_ID)
        #tile-ID eigenschappen assignen
        # for i in range(1,5):
        #     red_tile_ID_info = i
        #     print(red_tile_ID_info)

    bord.Screen.screen.blit(player_0, speler_pos)#blit de speler pion
    pygame.display.flip()
    clock.tick(60)
