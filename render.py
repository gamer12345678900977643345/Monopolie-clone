import pygame

def teken_alles(bord, posities, owned_pos_speler, owned_pos_bot, gevangen_beurten, paused, UI, clock):
    for i in range(0, 10, 9):#witte hoeken
        pygame.draw.rect(bord.Screen.screen, (255, 255, 255), (80*i+75,130,80,90))
        pygame.draw.rect(bord.Screen.screen, (255, 255, 255), (80*i+75,580,80,90))
        bord.Screen.screen.blit(UI.go_to_jail_, (75,130))
        bord.Screen.screen.blit(UI.font.render("START", True, (10,10,10)), (795,130))
        bord.Screen.screen.blit(UI.jail, (795, 580))
        bord.Screen.screen.blit(UI.parking, (75,580))
        pygame.draw.rect(bord.Screen.screen, (0, 0, 0), (80*i+75,130,80,90), 1)
        pygame.draw.rect(bord.Screen.screen, (0, 0, 0), (80*i+75,580,80,90), 1)
    
    # hieronder print alle vakken en straten op het scherm
    player_0 = pygame.image.load("assets/player0.png").convert_alpha()
    bot0 = pygame.image.load("assets/player1.png").convert_alpha()
    red_tile = pygame.image.load("assets/tile0.png").convert_alpha()
    green_tile = pygame.image.load("assets/tile1.png").convert_alpha()
    blue_tile = pygame.image.load("assets/tile2.png").convert_alpha()
    yellow_tile = pygame.image.load("assets/tile3.png").convert_alpha()
    font = pygame.font.SysFont("Tahoma", 30)
    
    for i in range(4):
        x = i * red_tile.get_width()
        y = 580
        bord.Screen.screen.blit(red_tile, (x+155,y))
    for i in range(4):
        x = 75 
        y = i *  green_tile.get_height()
        bord.Screen.screen.blit(green_tile, (x,y+220))
    for i in range(4):
        x = i * blue_tile.get_width()
        y = 130
        bord.Screen.screen.blit(blue_tile, (x+155,y))
    for i in range(4):
        x = 795 
        y = i *  yellow_tile.get_height()
        bord.Screen.screen.blit(yellow_tile, (x,y+220))
    
    # coordinaten regelen
    for i in range(1,9):
        x = i * blue_tile.get_width()
        y = 130
        red_tile_ID = (x, y)
    
    bord.Screen.screen.blit(player_0, (posities["speler"]["x"], posities["speler"]["y"]))
    bord.Screen.screen.blit(bot0, (posities["bot"]["x"], posities["bot"]["y"]))
    bord.Screen.screen.blit(font.render(f"Budget: {posities['speler']['budget']}", True, (230,230,230)), (200, 220))
    bord.Screen.screen.blit(font.render(f"Eigendommen: {posities['speler']['eigendom']}", True, (230,230,230)), (200,270))
    bord.Screen.screen.blit(font.render(f"Budget bot: {posities['bot']['budget']}", True, (230,230,230)), (200, 320))
    bord.Screen.screen.blit(font.render(f"Eigendommen bot: {posities['bot']['eigendom']}", True, (230,230,230)), (200,370))
    
    if gevangen_beurten["speler"] > 0:
        bord.Screen.screen.blit(font.render(f"GEVANGENIS: {gevangen_beurten['speler']} beurten", True, (255, 50, 50)), (200, 420))
    if gevangen_beurten["bot"] > 0:
        bord.Screen.screen.blit(font.render(f"BOT GEVANGENIS: {gevangen_beurten['bot']} beurten", True, (255, 50, 50)), (200, 470))
    
    for pos in owned_pos_speler:
        bord.Screen.screen.blit(UI.speler_owned, (pos["x"], pos["y"]))
        # Teken level als het bestaat
        if "level" in pos and pos["level"] > 0:
            bord.Screen.screen.blit(UI.small_font.render(str(pos["level"]), True, (255,255,255)), (pos["x"] + 14, pos["y"] + 9))

    for pos in owned_pos_bot:
        bord.Screen.screen.blit(UI.bot_owned, (pos["x"], pos["y"]))
        # Teken level als het bestaat
        if "level" in pos and pos["level"] > 0:
            bord.Screen.screen.blit(UI.small_font.render(str(pos["level"]), True, (255,255,255)), (pos["x"] + 14, pos["y"] + 9))
    
    # teken pauze menu als gepauzeerd
    if paused:
        UI.pause_menu()
    else:
        # teken menu knop alleen als niet gepauzeerd
        bord.Screen.screen.blit(UI.menu_knop, (600,0))
    
    pygame.display.flip()
    clock.tick(60)
# def animatie():
#     player_0 = pygame.image.load("assets/player0.png").convert_alpha()
#     bot0 = pygame.image.load("assets/player1.png").convert_alpha()

#     return