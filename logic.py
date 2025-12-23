import pygame
import random
def koop_mechanisme(bord, owned_pos_bot, owned_pos_speler, posities, huidige, font, vak, message_text, message_color, message_timer):
    koop_knop = pygame.draw.rect(bord.Screen.screen, (200,200,100), (900, 450,300,60))
    pygame.draw.rect(bord.Screen.screen, (80,20,20), (900, 450,300,60),5)
    bord.Screen.screen.blit(font.render("Koop nu", True, (230,230,230)), (910,460))
    # print(f"bot: {owned_pos_bot}")
    # print(f"speler: {owned_pos_speler}")
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if koop_knop.collidepoint(event.pos):
                if(posities[huidige]["budget"] >= vak["prijs"]):
                    vak["eigenaar"] = huidige
                    posities[huidige]["budget"] -= vak["prijs"]
                    posities[huidige]["eigendom"] += vak["prijs"]
                    owned_pos_speler.append({"x": posities["speler"]["x"], "y": posities["speler"]["y"], "waarde": vak["prijs"], "level": vak["level"]})
                    message_timer = 1000
                    if message_timer > 0:
                        bord.Screen.screen.blit(font.render(message_text, True, message_color), (500, 220))
                        message_text = f"-{vak["prijs"]}"
                        message_color = (255, 0, 0)
                        message_timer -= 1
                else:
                    bord.Screen.screen.blit(font.render("Niet genoeg geld!", True, (230,230,230)), (1200,250))
                    print("you broke!")
                    pygame.display.flip()
                    pygame.time.wait(1000)
    return message_text, message_color, message_timer

def move_logica(vakken_opgeschoven, posities, huidige, render, bord, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock):
    resterende_vakken = vakken_opgeschoven
    
    while resterende_vakken > 0:
        if posities[huidige]['straat'] == 'geel':
            vakken_tot_hoek = (580 - posities[huidige]["y"]) // 90
            
            if resterende_vakken <= vakken_tot_hoek:
                posities[huidige]["y"] += resterende_vakken * 90
                resterende_vakken = 0
            else:
                posities[huidige]["y"] = 580
                posities[huidige]['straat'] = 'rood'
                resterende_vakken -= (vakken_tot_hoek + 1)
        
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
                posities[huidige]["budget"] += 200
                posities[huidige]['straat'] = 'geel'
                resterende_vakken -= (vakken_tot_hoek + 1)
    
    render.teken_alles(bord, posities, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock)

def upgrade_mechanism(i, bord, upgrade_knop, posities, event, huidige, geluid, font, vak, UI, owned_pos_speler, owned_pos_bot, message_text, message_color, message_timer):
    """Returns updated i value"""
    pygame.draw.rect(bord.Screen.screen, (50,100,200), upgrade_knop)
    bord.Screen.screen.blit(UI.font.render("UPGRADE", True, (10,10,10)), upgrade_knop)
    pygame.draw.rect(bord.Screen.screen, (10,10,10), upgrade_knop, 2)
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if upgrade_knop.collidepoint(event.pos) and i < 1:
            if posities[huidige]["budget"] >= vak["upgrade"]:
                vak["huur"] += 10
                vak["level"] += 1  # Verhoog upgrade level
                posities[huidige]["budget"] -= vak["upgrade"]
                message_text = f"-{vak["upgrade"]}"
                message_color = (255, 0, 0)  # Groen
                message_timer = 5
                
                # Update level in owned_pos lijst
                if huidige == "speler":
                    geluid.player_upgrade.play()
                    for pos in owned_pos_speler:
                        if pos["x"] == posities["speler"]["x"] and pos["y"] == posities["speler"]["y"]:
                            pos["level"] = vak["level"]
                            break
                    
                i = 1
            else:
                bord.Screen.screen.blit(font.render("Niet genoeg geld!", True, (230,230,230)), (910, 590))
    
    return i, message_text, message_color, message_timer

def huur_mechanisme(i, betaler, ontvanger, vak, posities, owned_pos_speler, owned_pos_bot, data, geluid):
    """Betaal huur en return (i, game_state)"""
    huur = vak["huur"]
    game_state = "playing"
    
    if posities[betaler]["budget"] >= huur:
        posities[betaler]["budget"] -= huur
        posities[ontvanger]["budget"] += huur
        
        if ontvanger == "speler":
            geluid.get_rent.play()
        elif betaler == "speler":
            geluid.pay_rent.play()
        
        return (1, game_state)  # i = 1 om te voorkomen dat huur dubbel betaald wordt
    else:
        # Niet genoeg geld - verkoop eigendom
        if betaler == "speler":
            if owned_pos_speler:
                verkocht = owned_pos_speler.pop()
                posities["speler"]["budget"] += verkocht["waarde"]
                posities["speler"]["eigendom"] -= verkocht["waarde"]
                vak["level"] = 1
                for straat in data.values():
                    for v in straat:
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
                
                if posities["speler"]["budget"] >= huur:
                    posities["speler"]["budget"] -= huur
                    posities[ontvanger]["budget"] += huur
                    return (1, "playing")
                else:
                    return (1, "game_over_bot_wint")
            else:
                game_state = "game_over_bot_wint"
                return (1, game_state)
        
        elif betaler == "bot":
            if owned_pos_bot:
                verkocht = owned_pos_bot.pop()
                posities["bot"]["budget"] += verkocht["waarde"]
                posities["bot"]["eigendom"] -= verkocht["waarde"]
                vak["level"] = 1
                for straat in data.values():
                    for v in straat:
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
                
                if posities["bot"]["budget"] >= huur:
                    posities["bot"]["budget"] -= huur
                    posities[ontvanger]["budget"] += huur
                    return (1, "playing")
                else:
                    return (1, "game_over_speler_wint")
            else:
                game_state = "game_over_speler_wint"
                return (1, game_state)
    
    return (1, game_state)

def bot_upgrade(i, posities, vak, geluid, owned_pos_bot):
    """Bot upgrade logica - returns updated i"""
    if i < 1 and posities["bot"]["budget"] >= vak["upgrade"]:
        vak["huur"] += 10
        vak["level"] += 1  # Verhoog upgrade level
        posities["bot"]["budget"] -= vak["upgrade"]
        
        # Update level in owned_pos_bot lijst
        for pos in owned_pos_bot:
            if pos["x"] == posities["bot"]["x"] and pos["y"] == posities["bot"]["y"]:
                pos["level"] = vak["level"]
                break
        
        geluid.bot_upgtade.play()
        print(f"bot upgrade - level {vak['level']}")
        return 1
    return i

def bot_koop(posities, vak, owned_pos_bot):
    """Bot koop logica"""
    if vak["eigenaar"] is None and posities["bot"]["budget"] > vak["prijs"]:
        vak["eigenaar"] = "bot"
        posities["bot"]["budget"] -= vak["prijs"]
        posities["bot"]["eigendom"] += vak["prijs"]
        owned_pos_bot.append({
            "x": posities["bot"]["x"], 
            "y": posities["bot"]["y"], 
            "waarde": vak["prijs"],
            "level": vak["level"]
        })
def dobbelsteen(dob_keus):
    dobb = random.randint(1, dob_keus)
    return dobb
def check_budget(posities, owned_pos_speler, owned_pos_bot,vak):
    if posities["speler"]["budget"] <=0:
        verkocht = owned_pos_speler.pop()
        posities["speler"]["budget"] += verkocht["waarde"]
        posities["speler"]["eigendom"] -= verkocht["waarde"]
        vak["level"] = 0
    if posities["bot"]["budget"] <= 0:
        verkocht = owned_pos_bot.pop()
        posities["bot"]["budget"] += verkocht["waarde"]
        posities["bot"]["eigendom"] -= verkocht["waarde"]
        vak["level"]= 1