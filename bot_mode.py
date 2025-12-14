import pygame
import sys
import bord
import json
import random
import UI
import geluid
import effecten
import render
import logic
pygame.init()
def bot_game():
    tile_ID = "tileID.json"
    with open(tile_ID, 'r') as json_file:
        data = json.load(json_file)
    dobbelsteen_choose = True
    dob_keus = 6  # Default waarde (BELANGRIJK: moet bestaan voordat while loop start)
    while dobbelsteen_choose == True:
        UI.dobbelsteen_kies()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if UI.d4_rect.collidepoint(event.pos):
                    dob_keus = 4
                    dobbelsteen_choose = False
                if UI.d6_rect.collidepoint(event.pos):
                    dob_keus = 6
                    dobbelsteen_choose = False
                if UI.d8_rect.collidepoint(event.pos):
                    dob_keus = 8
                    dobbelsteen_choose = False
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
    geluid.background()
    
    
    
    i=0 #dit zorg dat de huur_mechanisme() maar 1 keer word uitgevoerd
    game_over_sound_played = False  # Aparte variabele voor game over geluid
    # Na posities = {...}
    speciale_vakken = {
        "ga_naar_gevangenis": {"x": 75, "y": 130},  
        "gevangenis": {"x": 795, "y": 580}
    }

    gevangen_beurten = {
        "speler": 0,
        "bot": 0
    }

    def check_speciale_vakken():
        nonlocal gevangen_beurten
        # Check "ga naar gevangenis" vak
        if (posities[huidige]["x"] == speciale_vakken["ga_naar_gevangenis"]["x"] and 
            posities[huidige]["y"] == speciale_vakken["ga_naar_gevangenis"]["y"]):
            
            print(f"{huidige} landt op 'Ga naar Gevangenis'!")
            
            # Teleporteer direct
            posities[huidige]["x"] = speciale_vakken["gevangenis"]["x"]
            posities[huidige]["y"] = speciale_vakken["gevangenis"]["y"]
            posities[huidige]["straat"] = "rood"
            
            gevangen_beurten[huidige] = 3
            print(f"{huidige} zit 3 beurten vast!")
    posities = {
        "speler": {"x": 795, "y": 130, 'straat' : 'geel', "budget": 1500, "eigendom": 0},
        "bot": {"x": 795, "y": 130, 'straat' : 'geel', "budget": 1500, "eigendom": 0}
    }
    message_timer = 0
    message_text = ""
    message_color = (230, 230, 230)
    clock = pygame.time.Clock()
    paused = False
    running = True
    while running:
        bord.Screen.screen.fill((75,170,75))#nice groen aub niet veranderen
        gooi_knop = pygame.draw.rect(bord.Screen.screen, (20,20,20), (950, 100, 100,100))
        bord.Screen.screen.blit(UI.menu_knop, (600,0))
        upgrade_knop = pygame.Rect(900,500,200,100)
        # speler_pos = (speler_pos_x, speler_pos_y)
        huidige = "bot" if beurt_num % 2 == 0 else "speler"
        # Check game state voor game over schermen
        if game_state == "game_over_bot_wint":
            # Teken game over scherm
            if not game_over_sound_played:
                geluid.player_los.play()
                game_over_sound_played = True
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
                        game_over_sound_played = False
                        beurt_num = 1
                        i = 0
                        posities["speler"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0} #reset de stats
                        posities["bot"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
                        owned_pos_speler.clear()
                        owned_pos_bot.clear()
                        gevangen_beurten["speler"] = 0
                        gevangen_beurten["bot"] = 0
                        for straat in data.values():
                            for vak in straat:
                                vak["eigenaar"] = None
                                vak["level"] = 1  # Reset level ook
            
            pygame.display.flip()
            clock.tick(60)
            continue  # skip rest van loop
        
        elif game_state == "game_over_speler_wint":
            # Teken win scherm
            if not game_over_sound_played:
                geluid.player_win.play()
                game_over_sound_played = True
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
                        game_over_sound_played = False
                        beurt_num = 1
                        i = 0
                        posities["speler"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
                        posities["bot"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
                        owned_pos_speler.clear()
                        owned_pos_bot.clear()
                        gevangen_beurten["speler"] = 0
                        gevangen_beurten["bot"] = 0
                        for straat in data.values():
                            for vak in straat:
                                vak["eigenaar"] = None
                                vak["level"] = 1  # Reset level ook
            
            pygame.display.flip()
            clock.tick(60)
            continue  # skip rest van loop
        
        for event in pygame.event.get():
            #tile info check (VERPLAATST BINNEN EVENT LOOP voor upgrade_mechanism)
            for vak in data['rood']:
                if posities[huidige]["x"] == vak["x"] and posities[huidige]['straat'] == 'rood':
                    # teken het info vak
                    info_screen()
                    
                    # koop-knop tonen als geen eigenaar
                    if vak["eigenaar"] is None:
                        if huidige == "speler":  # alleen speler ziet koop knop
                            message_text, message_color, message_timer = logic.koop_mechanisme(bord, owned_pos_bot, owned_pos_speler, posities, huidige, font, vak, message_text, message_color, message_timer)
                        
                    elif vak["eigenaar"] == "speler":
                        i, message_text, message_color, message_timer = logic.upgrade_mechanism(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler, owned_pos_bot, message_text, message_color, message_timer)                   
                    # check huur betaling
                    elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                        i, game_state = logic.huur_mechanisme(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler, owned_pos_bot, data, geluid)
                    
                        
            for vak in data['geel']:
                if posities[huidige]["y"] == vak["y"] and posities[huidige]['straat'] == 'geel':
                    # teken het info vak
                    info_screen()
                    
                    # koop-knop tonen als geen eigenaar
                    if vak["eigenaar"] is None:
                        if huidige == "speler":
                            message_text, message_color, message_timer = logic.koop_mechanisme(bord, owned_pos_bot, owned_pos_speler, posities, huidige, font, vak, message_text, message_color, message_timer)
                        
                    elif vak["eigenaar"] == "speler":
                        i, message_text, message_color, message_timer = logic.upgrade_mechanism(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler, owned_pos_bot, message_text, message_color, message_timer)
                    
                    # check huur betaling
                    elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                        i, game_state = logic.huur_mechanisme(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler, owned_pos_bot, data, geluid)

            for vak in data['groen']:
                if posities[huidige]["y"] == vak["y"] and posities[huidige]['straat'] == 'groen':
                    # teken het info vak
                    info_screen()
                    
                    # koop-knop tonen als geen eigenaar
                    if vak["eigenaar"] is None:
                        if huidige == "speler":
                            message_text, message_color, message_timer = logic.koop_mechanisme(bord, owned_pos_bot, owned_pos_speler, posities, huidige, font, vak, message_text, message_color, message_timer)
                            
                    elif vak["eigenaar"] == "speler":
                        i, message_text, message_color, message_timer = logic.upgrade_mechanism(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler, owned_pos_bot, message_text, message_color, message_timer)

                    # check huur betaling
                    elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                        i, game_state = logic.huur_mechanisme(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler, owned_pos_bot, data, geluid)

            for vak in data['blauw']:
                if posities[huidige]["x"] == vak["x"] and posities[huidige]['straat'] == 'blauw':
                    # teken het info vak
                    info_screen()
                    
                    # koop-knop tonen als geen eigenaar
                    if vak["eigenaar"] is None:
                        if huidige == "speler":
                            message_text, message_color, message_timer = logic.koop_mechanisme(bord, owned_pos_bot, owned_pos_speler, posities, huidige, font, vak, message_text, message_color, message_timer)

                    elif vak["eigenaar"] == "speler":
                        i, message_text, message_color, message_timer = logic.upgrade_mechanism(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler, owned_pos_bot, message_text, message_color, message_timer)

                    # check huur betaling
                    elif vak["eigenaar"] is not None and vak["eigenaar"] != huidige and i < 1:
                        i, game_state = logic.huur_mechanisme(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler, owned_pos_bot, data, geluid)

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
                        # Reset i aan begin van nieuwe beurt
                        i = 0
                        
                        # SPELER BEURT 
                        if gevangen_beurten["speler"] > 0:
                            gevangen_beurten["speler"] -= 1
                            print(f"Speler zit nog {gevangen_beurten['speler']} beurten gevangen")
                            beurt_num += 1
                        else:
                            dobb1 = logic.dobbelsteen(dob_keus)
                            dobb2 = logic.dobbelsteen(dob_keus)
                            geluid.dobb_eff.play()
                            geluid.move_eff.play()
                            dob_tot = dobb1 + dobb2
                            vakken_opgeschoven = dob_tot
                            dice_type = f'D{dob_keus}'  # Bijvoorbeeld 'D8'
                            bord.Screen.screen.blit(UI.dice_img[(dice_type, dobb1)], (950-400, 300))
                            bord.Screen.screen.blit(UI.dice_img[(dice_type, dobb2)], (1050-400, 300))
                            if dobb1 == dobb2:
                                print(f"BOT DUBBEL! {dobb1} en {dobb2}")
                                effect_num, effect_naam, vakken_beweging = effecten.random_effecten(huidige, posities, gevangen_beurten, owned_pos_speler, owned_pos_bot, 
                                        speciale_vakken, font, bord)
                                render.teken_alles(bord, posities, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock) 
                                pygame.display.flip()
                            # print(huidige)
                            # print(beurt_num)
                            logic.move_logica(vakken_opgeschoven, posities, huidige, render, bord, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock)
                            check_speciale_vakken()
                            beurt_num += 1
                        
                        render.teken_alles(bord, posities, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock)
                        pygame.draw.rect(bord.Screen.screen, (20,20,20), (950, 100, 100,100))
                        pygame.display.flip()
                        pygame.time.wait(750)

                        # Reset i voor bot beurt
                        i = 0

                        # BOT BEURT
                        huidige = "bot"
                        if gevangen_beurten["bot"] > 0:
                            gevangen_beurten["bot"] -= 1
                            print(f"Bot zit nog {gevangen_beurten['bot']} beurten gevangen")
                            beurt_num += 1
                        else:
                            dobb1 = logic.dobbelsteen(dob_keus)
                            dobb2 = logic.dobbelsteen(dob_keus)
                            geluid.dobb_eff.play()
                            geluid.move_eff.play()
                            dob_tot = dobb1 + dobb2
                            dice_type = f'D{dob_keus}'  # Bijvoorbeeld 'D8'
                            bord.Screen.screen.blit(UI.dice_img[(dice_type, dobb1)], (950-400, 300))
                            bord.Screen.screen.blit(UI.dice_img[(dice_type, dobb2)], (1050-400, 300))
                            if dobb1 == dobb2:
                                print(f"BOT DUBBEL! {dobb1} en {dobb2}")
                                effect_num, effect_naam, vakken_beweging = effecten.random_effecten(huidige, posities, gevangen_beurten, owned_pos_speler, owned_pos_bot, 
                                        speciale_vakken, font, bord)
                                render.teken_alles(bord, posities, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock)
                                pygame.display.flip()
                            vakken_opgeschoven = dob_tot
                            # print(huidige)
                            # print(beurt_num)
                        
                            logic.move_logica(vakken_opgeschoven, posities, huidige, render, bord, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock)  # ← hier beweegt bot
                            check_speciale_vakken()  # ← check of bot op speciaal vak staat
                            if posities["bot"]["straat"] in data:  # ← voeg deze check toe
                                for vak in data[posities["bot"]["straat"]]:
                                    # Bepaal of bot op dit vak staat
                                    op_vak = False
                                    if posities["bot"]["straat"] == "rood" or posities["bot"]["straat"] == "blauw":
                                        op_vak = (posities["bot"]["x"] == vak["x"])
                                    elif posities["bot"]["straat"] == "geel" or posities["bot"]["straat"] == "groen":
                                        op_vak = (posities["bot"]["y"] == vak["y"])
                                    
                                    if op_vak:
                                        # Bot koop logica
                                        logic.bot_koop(posities, vak, owned_pos_bot)
                                        
                                        # Bot huur betalen
                                        if vak["eigenaar"] == "speler" and i < 1:
                                            i, game_state = logic.huur_mechanisme(i, "bot", "speler", vak, posities, owned_pos_speler, owned_pos_bot, data, geluid)
                                            break
                                        
                                        # Bot upgrade
                                        elif vak["eigenaar"] == "bot" and i < 1:
                                            i = logic.bot_upgrade(i, posities, vak, geluid, owned_pos_bot)
                                            break
                            
                            beurt_num += 1  # ← voeg dit toe na bot zet
                        pygame.time.wait(750)
                elif paused:  # check pauze menu knoppen
                    if UI.exit_knop_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if UI.continue_knop_rect.collidepoint(event.pos):
                        paused = False

        # print(f"budget speler: {"speler"}, budget bot: {"bot"}, huur: {posities}")

        # Teken bericht als timer actief is (AAN HET EINDE)
        if message_timer > 0:
            bord.Screen.screen.blit(font.render(message_text, True, message_color), (500, 220))
            message_timer -= 1

        render.teken_alles(bord, posities, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock)
        # logic.check_budget(posities, owned_pos_speler, owned_pos_bot, vak)  # VERWIJDERD: 'vak' bestaat niet hier
        pygame.display.flip()
        clock.tick(60)  # Voeg clock.tick toe voor frame limiet