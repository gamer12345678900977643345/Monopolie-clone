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
import player

pygame.init()

def pvp_game():
    tile_ID = "tileID.json"
    with open(tile_ID, 'r') as json_file:
        data = json.load(json_file)
    
    # Verkrijg spelersnamen
    naam1 = UI.start_settings()
    naam2 = UI.start_settings()
    
    # Dobbelsteenkeuze
    dobbelsteen_choose = True
    while dobbelsteen_choose:
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
    
    font = pygame.font.SysFont("Tahoma", 30)
    
    def info_screen():
        pygame.draw.rect(bord.Screen.screen, (188, 180, 162), (900, 200, 300, 240))
        pygame.draw.rect(bord.Screen.screen, (80, 20, 20), (900, 200, 300, 240), 5)
        bord.Screen.screen.blit(font.render(vak["naam"], True, (230, 230, 230)), (910, 220))
        bord.Screen.screen.blit(font.render(f"Prijs: {vak['prijs']}", True, (230, 230, 230)), (910, 260))
        bord.Screen.screen.blit(font.render(f"Huur: {vak['huur']}", True, (230, 230, 230)), (910, 300))
        bord.Screen.screen.blit(font.render(f"Upgrade: {vak['upgrade']}", True, (230, 230, 230)), (910, 340))
        bord.Screen.screen.blit(font.render(f"Eigenaar: {vak['eigenaar']}", True, (230, 230, 230)), (910, 380))
    
    beurt_num = 1
    owned_pos_speler1 = []
    owned_pos_speler2 = []
    game_state = "playing"
    geluid.background()
    
    i = 0
    game_over_sound_played = False
    
    speciale_vakken = {
        "ga_naar_gevangenis": {"x": 75, "y": 130},
        "gevangenis": {"x": 795, "y": 580}
    }
    
    gevangen_beurten = {
        "speler1": 0,
        "speler2": 0
    }
    
    def check_speciale_vakken():
        nonlocal gevangen_beurten
        if (posities[huidige]["x"] == speciale_vakken["ga_naar_gevangenis"]["x"] and 
            posities[huidige]["y"] == speciale_vakken["ga_naar_gevangenis"]["y"]):
            posities[huidige]["x"] = speciale_vakken["gevangenis"]["x"]
            posities[huidige]["y"] = speciale_vakken["gevangenis"]["y"]
            posities[huidige]["straat"] = "rood"
            gevangen_beurten[huidige] = 3
    
    posities = {
        "speler1": {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0},
        "speler2": {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
    }
    
    message_timer = 0
    message_text = ""
    message_color = (230, 230, 230)
    clock = pygame.time.Clock()
    paused = False
    running = True
    
    while running:
        bord.Screen.screen.fill((75, 170, 75))
        gooi_knop = pygame.draw.rect(bord.Screen.screen, (20, 20, 20), (950, 100, 100, 100))
        bord.Screen.screen.blit(UI.menu_knop, (600, 0))
        upgrade_knop = pygame.Rect(900, 500, 200, 100)
        
        huidige = "speler2" if beurt_num % 2 == 0 else "speler1"
        andere = "speler1" if huidige == "speler2" else "speler2"
        
        # ...game over checks...
        if game_state == "game_over_speler1_wint":
            if not game_over_sound_played:
                geluid.player_win.play()
                game_over_sound_played = True
            UI.end_screen_win()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if UI.replay_knop.collidepoint(pygame.mouse.get_pos()) if event.type == pygame.MOUSEBUTTONDOWN else False:
                        game_state = "playing"
                        game_over_sound_played = False
                        beurt_num = 1
                        i = 0
                        posities["speler1"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
                        posities["speler2"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
                        owned_pos_speler1.clear()
                        owned_pos_speler2.clear()
                        gevangen_beurten["speler1"] = 0
                        gevangen_beurten["speler2"] = 0
                        for straat in data.values():
                            for vak in straat:
                                vak["eigenaar"] = None
                    else:
                        return
            pygame.display.flip()
            clock.tick(60)
            continue
        
        elif game_state == "game_over_speler2_wint":
            if not game_over_sound_played:
                geluid.player_los.play()
                game_over_sound_played = True
            UI.end_screen_loss()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if UI.replay_knop.collidepoint(pygame.mouse.get_pos()) if event.type == pygame.MOUSEBUTTONDOWN else False:
                        game_state = "playing"
                        game_over_sound_played = False
                        beurt_num = 1
                        i = 0
                        posities["speler1"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
                        posities["speler2"] = {"x": 795, "y": 130, 'straat': 'geel', "budget": 1500, "eigendom": 0}
                        owned_pos_speler1.clear()
                        owned_pos_speler2.clear()
                        gevangen_beurten["speler1"] = 0
                        gevangen_beurten["speler2"] = 0
                        for straat in data.values():
                            for vak in straat:
                                vak["eigenaar"] = None
                    else:
                        return
            pygame.display.flip()
            clock.tick(60)
            continue
        
        # Tile info checks
        for vak in data['rood']:
            if posities[huidige]["x"] == vak["x"] and posities[huidige]['straat'] == 'rood':
                info_screen()
                if vak["eigenaar"] is None:
                    message_text, message_color, message_timer = logic.koop_mechanisme_pvp(bord, owned_pos_speler1, owned_pos_speler2, posities, huidige, font, vak, message_text, message_color, message_timer)
                elif vak["eigenaar"] == huidige:
                    i, message_text, message_color, message_timer = logic.upgrade_mechanism_pvp(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler1, owned_pos_speler2, message_text, message_color, message_timer)
                elif vak["eigenaar"] != huidige and i < 1:
                    i, game_state = logic.huur_mechanisme_pvp(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler1, owned_pos_speler2, data, geluid)
        
        for vak in data['geel']:
            if posities[huidige]["y"] == vak["y"] and posities[huidige]['straat'] == 'geel':
                info_screen()
                if vak["eigenaar"] is None:
                    message_text, message_color, message_timer = logic.koop_mechanisme_pvp(bord, owned_pos_speler2, owned_pos_speler1, posities, huidige, font, vak, message_text, message_color, message_timer)
                elif vak["eigenaar"] == huidige:
                    i, message_text, message_color, message_timer = logic.upgrade_mechanism_pvp(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler1, owned_pos_speler2, message_text, message_color, message_timer)
                elif vak["eigenaar"] != huidige and i < 1:
                    i, game_state = logic.huur_mechanisme_pvp(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler1, owned_pos_speler2, data, geluid)
        
        for vak in data['groen']:
            if posities[huidige]["y"] == vak["y"] and posities[huidige]['straat'] == 'groen':
                info_screen()
                if vak["eigenaar"] is None:
                    message_text, message_color, message_timer = logic.koop_mechanisme_pvp(bord, owned_pos_speler2, owned_pos_speler1, posities, huidige, font, vak, message_text, message_color, message_timer)
                elif vak["eigenaar"] == huidige:
                    i, message_text, message_color, message_timer = logic.upgrade_mechanism_pvp(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler1, owned_pos_speler2, message_text, message_color, message_timer)
                elif vak["eigenaar"] != huidige and i < 1:
                    i, game_state = logic.huur_mechanisme_pvp(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler1, owned_pos_speler2, data, geluid)
        
        for vak in data['blauw']:
            if posities[huidige]["x"] == vak["x"] and posities[huidige]['straat'] == 'blauw':
                info_screen()
                if vak["eigenaar"] is None:
                    message_text, message_color, message_timer = logic.koop_mechanisme_pvp(bord, owned_pos_speler2, owned_pos_speler1, posities, huidige, font, vak, message_text, message_color, message_timer)
                elif vak["eigenaar"] == huidige:
                    i, message_text, message_color, message_timer = logic.upgrade_mechanism_pvp(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler1, owned_pos_speler2, message_text, message_color, message_timer)
                elif vak["eigenaar"] != huidige and i < 1:
                    i, game_state = logic.huur_mechanisme_pvp(i, huidige, vak["eigenaar"], vak, posities, owned_pos_speler1, owned_pos_speler2, data, geluid)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if UI.menu_knop_rect.collidepoint(event.pos):
                    paused = not paused
                elif not paused and gooi_knop.collidepoint(event.pos):
                    i = 0
                    if gevangen_beurten[huidige] > 0:
                        gevangen_beurten[huidige] -= 1
                        beurt_num += 1
                    else:
                        dobb1 = logic.dobbelsteen(dob_keus)
                        dobb2 = logic.dobbelsteen(dob_keus)
                        geluid.dobb_eff.play()
                        geluid.move_eff.play()
                        dob_tot = dobb1 + dobb2
                        dice_type = f'D{dob_keus}'
                        vakken_opgeschoven = dob_tot
                        bord.Screen.screen.blit(UI.dice_img[(dice_type, dobb1)], (950 - 400, 300))
                        bord.Screen.screen.blit(UI.dice_img[(dice_type, dobb2)], (1050 - 400, 300))
                        logic.move_logica_pvp(vakken_opgeschoven, posities, huidige, render, bord, owned_pos_speler1, owned_pos_speler2, gevangen_beurten, paused, UI, clock, player)
                        check_speciale_vakken()
                        beurt_num += 1
                        print(f"huidige: {huidige}")
                        print(f"speler1: eigendom {owned_pos_speler1}")
                        print(f"speler2: eigendom {owned_pos_speler2}")

                    render.teken_alles_pvp(bord, posities, owned_pos_speler1, owned_pos_speler2, gevangen_beurten, paused, UI, clock, player)
                    pygame.time.wait(750)
                elif paused:
                    if UI.exit_knop_rect.collidepoint(event.pos):
                        return
                    if UI.continue_knop_rect.collidepoint(event.pos):
                        paused = False
        render.teken_alles_pvp(bord, posities, owned_pos_speler1, owned_pos_speler2, gevangen_beurten, paused, UI, clock, player)
        pygame.display.flip()
        clock.tick(60)