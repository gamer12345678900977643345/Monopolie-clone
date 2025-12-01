import pygame
import sys
import bord
import json
import random
import UI
import geluid
pygame.init()
def bot_game():
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
    beurt_num = 1
    def koop_mechanisme():
        koop_knop = pygame.draw.rect(bord.Screen.screen, (200,200,100), (900, 450,300,60))
        pygame.draw.rect(bord.Screen.screen, (80,20,20), (900, 450,300,60),5)
        bord.Screen.screen.blit(font.render("Koop nu", True, (230,230,230)), (910,460))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if koop_knop.collidepoint(event.pos):
                if(posities[huidige]["budget"] > vak["prijs"]):
                    vak["eigenaar"] = huidige
                    posities[huidige]["budget"] -= vak["prijs"]
                    posities[huidige]["eigendom"] += vak["prijs"]
                    # print(player.speler1.balans)
                else:
                    bord.Screen.screen.blit(font.render("Niet genoeg geld!", True, (230,230,230)), (1200,250))
                    print("you broke!")
                    pygame.display.flip()
                    pygame.time.wait(1000)
        return

    geluid.background()

    posities = {
        "speler": {"x": 795, "y": 130, 'straat' : 'geel', "budget": 1500, "eigendom": 0},
        "bot": {"x": 795, "y": 130, 'straat' : 'geel', "budget": 1500, "eigendom": 0}
    }
    clock = pygame.time.Clock()
    net_gegooid = False
    paused = False
    running = True
    while running:
        bord.Screen.screen.fill((75,170,75))#nice groen aub niet veranderen
        # speler_pos = (speler_pos_x, speler_pos_y)
        huidige = "bot" if beurt_num % 2 == 0 else "speler"
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
                        geluid.dobbelsteen_effect()
                        geluid.move_effect()
                        dob_tot = dobb1 + dobb2
                        vakken_opgeschoven = dob_tot #moet spitsen naar x en y en in loop toevoegen
                        net_gegooid = True
                        print(huidige)
                        print(beurt_num)
                        #speler beweegt langs gele straat
                        if posities[huidige]['straat'] == 'geel':
                            posities[huidige]["y"] += vakken_opgeschoven*90
                            if posities[huidige]["y"] > 580:
                                posities[huidige]["y"] = 580
                                posities[huidige]['straat'] = 'rood'
                        
                        elif posities[huidige]['straat'] == 'rood':
                            posities[huidige]["x"] -= vakken_opgeschoven*80
                            if posities[huidige]["x"] < 75:
                                posities[huidige]["x"] = 75
                                posities[huidige]['straat'] = 'groen'
                        
                        elif posities[huidige]['straat'] == 'groen':
                            posities[huidige]["y"] -= vakken_opgeschoven*90
                            if posities[huidige]["y"] < 130:
                                posities[huidige]["y"] = 130
                                posities[huidige]['straat'] = 'blauw'
                        
                        elif posities[huidige]['straat'] == 'blauw':
                            posities[huidige]["x"] += vakken_opgeschoven*80
                            if posities[huidige]["x"] > 795:
                                posities[huidige]["x"] = 795
                                posities[huidige]["budget"] += 200
                                posities[huidige]['straat']= 'geel'
                        beurt_num +=1
                        
                        # print(speler_pos)
                elif paused:  # check pauze menu knoppen
                    if UI.exit_knop_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if UI.continue_knop_rect.collidepoint(event.pos):
                        paused = False

        #tile info check
        for vak in data['rood']:
            kleur_x = vak["x"]
            if posities[huidige]["x"] == kleur_x and posities[huidige]['straat'] == 'rood':
                # teken het info vak
                info_screen()
                # koop-knop tonen als geen eigenaar
                if vak["eigenaar"] is None:
                    koop_mechanisme()
        
        for vak in data['geel']:
            kleur_y = vak["y"]
            if posities[huidige]["y"] == kleur_y and posities[huidige]['straat'] == 'geel':
                # teken het info vak
                info_screen()
                # koop-knop tonen als geen eigenaar
                if vak["eigenaar"] is None:
                    koop_mechanisme()
        
        for vak in data['groen']:
            kleur_y = vak["y"]
            if posities[huidige]["y"] == kleur_y and posities[huidige]['straat'] == 'groen':
                # teken het info vak
                info_screen()
                # koop-knop tonen als geen eigenaar
                if vak["eigenaar"] is None:
                    koop_mechanisme()
        
        for vak in data['blauw']:
            kleur_x = vak["x"]
            if posities[huidige]["x"] == kleur_x and posities[huidige]['straat'] == 'blauw':
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
        bot0 = pygame.image.load("assets/player1.png").convert_alpha()
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
        
        bord.Screen.screen.blit(player_0, (posities["speler"]["x"], posities["speler"]["y"]))#blit de speler pion
        bord.Screen.screen.blit(bot0, (posities["bot"]["x"], posities["bot"]["y"]))
        bord.Screen.screen.blit(font.render(f"Budget: {posities["speler"]["budget"]}", True, (230,230,230)), (1200, 150))
        bord.Screen.screen.blit(font.render(f"Eigendommen: {posities["speler"]["eigendom"]}", True, (230,230,230)), (1200,200))
        bord.Screen.screen.blit(font.render(f"Budget bot: {posities["bot"]["budget"]}", True, (230,230,230)), (1200, 250))
        bord.Screen.screen.blit(font.render(f"Eigendommen bot: {posities["bot"]["eigendom"]}", True, (230,230,230)), (1200,300))
        # teken pauze menu als gepauzeerd
        if paused:
            UI.pause_menu()
        else:
            # teken menu knop alleen als niet gepauzeerd
            bord.Screen.screen.blit(UI.menu_knop, (600,0))
        
        pygame.display.flip()
        clock.tick(60)