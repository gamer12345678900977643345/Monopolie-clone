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
    owned_pos_speler = []
    owned_pos_bot = []
    game_state = "playing"  # nieuwe variabele voor game state
    def koop_mechanisme():
        koop_knop = pygame.draw.rect(bord.Screen.screen, (200,200,100), (900, 450,300,60))
        pygame.draw.rect(bord.Screen.screen, (80,20,20), (900, 450,300,60),5)
        bord.Screen.screen.blit(font.render("Koop nu", True, (230,230,230)), (910,460))
        print(f"bot: {owned_pos_bot}")
        print(f"speler: {owned_pos_speler}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if koop_knop.collidepoint(event.pos):
                if(posities[huidige]["budget"] >= vak["prijs"]):
                    vak["eigenaar"] = huidige
                    posities[huidige]["budget"] -= vak["prijs"]
                    posities[huidige]["eigendom"] += vak["prijs"]
                    owned_pos_speler.append({"x": posities["speler"]["x"], "y": posities["speler"]["y"], "waarde": vak["prijs"]})
                else:
                    bord.Screen.screen.blit(font.render("Niet genoeg geld!", True, (230,230,230)), (1200,250))
                    print("you broke!")
                    pygame.display.flip()
                    pygame.time.wait(1000)
        return

    geluid.background()
    def move_logica():
        resterende_vakken = vakken_opgeschoven
        
        while resterende_vakken > 0:
            if posities[huidige]['straat'] == 'geel':
                # Bereken hoeveel vakken er nog zijn tot de hoek
                vakken_tot_hoek = (580 - posities[huidige]["y"]) // 90
                
                if resterende_vakken <= vakken_tot_hoek:
                    # Kan volledig bewegen zonder hoek te raken
                    posities[huidige]["y"] += resterende_vakken * 90
                    resterende_vakken = 0
                else:
                    # Gaat over de hoek heen
                    posities[huidige]["y"] = 580
                    posities[huidige]['straat'] = 'rood'
                    resterende_vakken -= (vakken_tot_hoek + 1)  # +1 voor de hoek
            
            elif posities[huidige]['straat'] == 'rood':
                vakken_tot_hoek = (posities[huidige]["x"] - 75) // 80
                
                if resterende_vakken <= vakken_tot_hoek:
                    posities[huidige]["x"] -= resterende_vakken * 80
                    resterende_vakken = 0
                else:
                    posities[huidige]["x"] = 75
                    posities[huidige]['straat'] = 'groen'
                    resterende_vakken -= (vakken_tot_hoek + 1)
            
            elif posities[huidige]['straat'] == 'groen':
                vakken_tot_hoek = (posities[huidige]["y"] - 130) // 90
                
                if resterende_vakken <= vakken_tot_hoek:
                    posities[huidige]["y"] -= resterende_vakken * 90
                    resterende_vakken = 0
                else:
                    posities[huidige]["y"] = 130
                    posities[huidige]['straat'] = 'blauw'
                    resterende_vakken -= (vakken_tot_hoek + 1)
            
            elif posities[huidige]['straat'] == 'blauw':
                vakken_tot_hoek = (795 - posities[huidige]["x"]) // 80
                
                if resterende_vakken <= vakken_tot_hoek:
                    posities[huidige]["x"] += resterende_vakken * 80
                    resterende_vakken = 0
                else:
                    posities[huidige]["x"] = 795
                    posities[huidige]["budget"] += 200  # start bonus
                    posities[huidige]['straat'] = 'geel'
                    resterende_vakken -= (vakken_tot_hoek + 1)
    def teken_alles():
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
        bord.Screen.screen.blit(font.render(f"Budget: {posities["speler"]["budget"]}", True, (230,230,230)), (200, 220))
        bord.Screen.screen.blit(font.render(f"Eigendommen: {posities["speler"]["eigendom"]}", True, (230,230,230)), (200,270))
        bord.Screen.screen.blit(font.render(f"Budget bot: {posities["bot"]["budget"]}", True, (230,230,230)), (200, 320))
        bord.Screen.screen.blit(font.render(f"Eigendommen bot: {posities["bot"]["eigendom"]}", True, (230,230,230)), (200,370))
        for pos in owned_pos_speler:
            bord.Screen.screen.blit(UI.speler_owned, (pos["x"], pos["y"]))

        for pos in owned_pos_bot:
            bord.Screen.screen.blit(UI.bot_owned, (pos["x"], pos["y"]))
        # teken pauze menu als gepauzeerd
        if paused:
            UI.pause_menu()
        else:
            # teken menu knop alleen als niet gepauzeerd
            bord.Screen.screen.blit(UI.menu_knop, (600,0))
        
        pygame.display.flip()
        clock.tick(60)
    def huur_mechanisme(betaler, ontvanger, vak):
        nonlocal game_state  # toegang tot game_state variabele
        huur = vak["huur"]    
        
        if posities[betaler]["budget"] >= huur:
            # Genoeg geld - betaal normaal
            posities[betaler]["budget"] -= huur
            posities[ontvanger]["budget"] += huur
            
            if ontvanger == "speler":
                geluid.get_rent.play()
            elif betaler == "speler":
                geluid.pay_rent.play()
        else:
            # Niet genoeg geld - check wie betaler is en verkoop eigendom
            if betaler == "speler":
                # Speler moet betalen maar heeft niet genoeg
                if owned_pos_speler:
                    # Verkoop een eigendom
                    verkocht = owned_pos_speler.pop()
                    posities["speler"]["budget"] += verkocht["waarde"]
                    posities["speler"]["eigendom"] -= verkocht["waarde"]
                    
                    # Vind het vak dat verkocht wordt en reset eigenaar
                    for straat in data.values():
                        for v in straat:
                            # Check x OF y afhankelijk van wat bestaat
                            match = False
                            if "x" in v and "x" in verkocht:
                                if v["x"] == verkocht["x"]:
                                    match = True
                            if "y" in v and "y" in verkocht:
                                if v["y"] == verkocht["y"]:
                                    match = True
                            
                            if match:
                                v["eigenaar"] = None
                                break
                    
                    # Probeer opnieuw huur te betalen
                    if posities["speler"]["budget"] >= huur:
                        posities["speler"]["budget"] -= huur
                        posities[ontvanger]["budget"] += huur
                else:
                    # Geen eigendommen meer - failliet
                    game_state = "game_over_bot_wint"
            
            elif betaler == "bot":
                # Bot moet betalen maar heeft niet genoeg
                if owned_pos_bot:
                    # Verkoop een eigendom
                    verkocht = owned_pos_bot.pop()
                    posities["bot"]["budget"] += verkocht["waarde"]
                    posities["bot"]["eigendom"] -= verkocht["waarde"]
                    
                    # Reset eigenaar van verkocht vak
                    for straat in data.values():
                        for v in straat:
                            # Check x OF y afhankelijk van wat bestaat
                            match = False
                            if "x" in v and "x" in verkocht:
                                if v["x"] == verkocht["x"]:
                                    match = True
                            if "y" in v and "y" in verkocht:
                                if v["y"] == verkocht["y"]:
                                    match = True
                            
                            if match:
                                v["eigenaar"] = None
                                break
                    
                    # Probeer opnieuw huur te betalen
                    if posities["bot"]["budget"] >= huur:
                        posities["bot"]["budget"] -= huur
                        posities[ontvanger]["budget"] += huur
                else:
                    # Geen eigendommen meer - failliet
                    game_state = "game_over_speler_wint"
    
    posities = {
        "speler": {"x": 795, "y": 130, 'straat' : 'geel', "budget": 1500, "eigendom": 0},
        "bot": {"x": 795, "y": 130, 'straat' : 'geel', "budget": 1500, "eigendom": 0}
    }
    i=0 #dit zorg dat de huur_mechanisme() maar 1 keer word uitgevoerd
    clock = pygame.time.Clock()
    paused = False
    running = True
    while running:
        bord.Screen.screen.fill((75,170,75))#nice groen aub niet veranderen
        # speler_pos = (speler_pos_x, speler_pos_y)
        huidige = "bot" if beurt_num % 2 == 0 else "speler"
        
        # Check game state voor game over schermen
        if game_state == "game_over_bot_wint":
            # Teken game over scherm
            UI.end_screen_loss()
            # Check voor exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running = False  # druk op toets om te sluiten
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if UI.replay_knop.collidepoint(event.pos):
                        # Reset alles
                        game_state = "playing"
                        beurt_num = 1
                        posities["speler"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 500, "eigendom": 0}
                        posities["bot"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 500, "eigendom": 0}
                        owned_pos_speler.clear()
                        owned_pos_bot.clear()
            
            pygame.display.flip()
            clock.tick(60)
            continue  # skip rest van loop
        
        elif game_state == "game_over_speler_wint":
            # Teken win scherm
            UI.end_screen_win()# Check voor exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if UI.replay_knop.collidepoint(event.pos):
                        # Reset alles
                        game_state = "playing"
                        beurt_num = 1
                        posities["speler"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 500, "eigendom": 0}
                        posities["bot"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 500, "eigendom": 0}
                        owned_pos_speler.clear()
                        owned_pos_bot.clear()
            
            pygame.display.flip()
            clock.tick(60)
            continue  # skip rest van loop
        
        #tile info check
        for vak in data['rood']:
            if posities[huidige]["x"] == vak["x"] and posities[huidige]['straat'] == 'rood':
                # teken het info vak
                info_screen()
                
                # koop-knop tonen als geen eigenaar
                if vak["eigenaar"] is None:
                    if huidige == "speler":  # alleen speler ziet koop knop
                        koop_mechanisme()
                
                # check huur betaling
                elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                    huur_mechanisme(huidige, vak["eigenaar"], vak)
                    i+=1
                    
        for vak in data['geel']:
            if posities[huidige]["y"] == vak["y"] and posities[huidige]['straat'] == 'geel':
                # teken het info vak
                info_screen()
                
                # koop-knop tonen als geen eigenaar
                if vak["eigenaar"] is None:
                    if huidige == "speler":
                        koop_mechanisme()
                
                # check huur betaling
                elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                    huur_mechanisme(huidige, vak["eigenaar"], vak)
                    i+=1

        for vak in data['groen']:
            if posities[huidige]["y"] == vak["y"] and posities[huidige]['straat'] == 'groen':
                # teken het info vak
                info_screen()
                
                # koop-knop tonen als geen eigenaar
                if vak["eigenaar"] is None:
                    if huidige == "speler":
                        koop_mechanisme()
                
                # check huur betaling
                elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                    huur_mechanisme(huidige, vak["eigenaar"], vak)
                    i+=1

        for vak in data['blauw']:
            if posities[huidige]["x"] == vak["x"] and posities[huidige]['straat'] == 'blauw':
                # teken het info vak
                info_screen()
                
                # koop-knop tonen als geen eigenaar
                if vak["eigenaar"] is None:
                    if huidige == "speler":
                        koop_mechanisme()
                
                # check huur betaling
                elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                    huur_mechanisme(huidige, vak["eigenaar"], vak)
                    i+=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # speler turn dobbelsteen gooien
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check menu knop eerst
                if UI.menu_knop_rect.collidepoint(event.pos):
                    paused = not paused  # toggle pauze status
                elif not paused and huidige == "speler":  # alleen andere knoppen als niet gepauzeerd
                    if gooi_knop.collidepoint(event.pos):
                        dobb1=dobbelsteen()
                        dobb2=dobbelsteen()
                        geluid.dobb_eff.play()
                        geluid.move_eff.play()
                        dob_tot = dobb1 + dobb2
                        vakken_opgeschoven = dob_tot #moet spitsen naar x en y en in loop toevoegen
                        print(huidige)
                        print(beurt_num)
                        #speler beweegt langs gele straat
                        move_logica()
                        i=0
                        beurt_num +=1
                        teken_alles()
                        pygame.draw.rect(bord.Screen.screen, (20,20,20), (950, 100, 100,100))
                        pygame.display.flip()
                        pygame.time.wait(1000)

                        huidige = "bot"
                        dobb1=dobbelsteen()
                        dobb2=dobbelsteen()
                        geluid.dobb_eff.play()
                        geluid.move_eff.play()
                        dob_tot = dobb1 + dobb2
                        vakken_opgeschoven = dob_tot #moet spitsen naar x en y en in loop toevoegen
                        print(huidige)
                        print(beurt_num)
                        #speler beweegt langs gele straat
                        move_logica()
                        i=0
                        
                        for vak in data[posities["bot"]["straat"]]:
                            if posities["bot"]["straat"] == "rood" or posities["bot"]["straat"] == "blauw":
                                if posities["bot"]["x"] == vak["x"]:
                                    if vak["eigenaar"] is None:
                                        if posities["bot"]["budget"] > vak["prijs"]:
                                            vak["eigenaar"] = "bot"
                                            posities["bot"]["budget"] -= vak["prijs"]
                                            posities["bot"]["eigendom"] += vak["prijs"]
                                            owned_pos_bot.append({"x" : posities["bot"]["x"], "y": posities["bot"]["y"], "waarde": vak["prijs"]})

                            elif posities["bot"]["straat"] == "geel" or posities["bot"]["straat"] == "groen":
                                if posities["bot"]["y"] == vak["y"]:
                                    if vak["eigenaar"] is None:
                                        if posities["bot"]["budget"] > vak["prijs"]:
                                            vak["eigenaar"] = "bot"
                                            posities["bot"]["budget"] -= vak["prijs"]
                                            posities["bot"]["eigendom"] += vak["prijs"]
                                            owned_pos_bot.append({"x" : posities["bot"]["x"], "y": posities["bot"]["y"], "waarde": vak["prijs"]})

                        for vak in data[posities["bot"]["straat"]]:
                            op_vak = False
                            
                            if posities["bot"]["straat"] in ["rood", "blauw"]:
                                op_vak = (posities["bot"]["x"] == vak["x"])
                            elif posities["bot"]["straat"] in ["geel", "groen"]:
                                op_vak = (posities["bot"]["y"] == vak["y"])
                            
                            if op_vak and vak["eigenaar"] == "speler":
                                huur_mechanisme("bot", "speler", vak)
                                break
                        beurt_num += 1
                    # print(speler_pos)
                elif paused:  # check pauze menu knoppen
                    if UI.exit_knop_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if UI.continue_knop_rect.collidepoint(event.pos):
                        paused = False

        # print(f"budget speler: {"speler"}, budget bot: {"bot"}, huur: {posities}")
        gooi_knop = pygame.draw.rect(bord.Screen.screen, (20,20,20), (950, 100, 100,100))

        teken_alles()