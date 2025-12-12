import pygame
import random

def random_effecten(huidige, posities, gevangen_beurten, owned_pos_speler, owned_pos_bot, 
                    speciale_vakken, font, bord):
    effect_num = random.randint(1, 10)
    effect_naam = ""
    vakken_beweging = 0
    tegenstander = "bot" if huidige == "speler" else "speler"
    if effect_num == 1:
        effect_naam = "go to jail"
        posities[huidige]["x"] = speciale_vakken["gevangenis"]["x"]
        posities[huidige]["y"] = speciale_vakken["gevangenis"]["y"]
        posities[huidige]["straat"] = "rood"
        gevangen_beurten[huidige] = 3
    elif effect_num == 2:
        effect_naam = "geef tegenstande 100"
        posities[huidige]["budget"] -= 100
        posities[tegenstander]["budget"] +=100
    elif effect_num == 3:
        effect_naam = "krijg 200 van de bank"
        posities[huidige]["budget"] += 200
    elif effect_num == 4:
        effect_naam = "betaal 150 aan de bank"
        posities[huidige]["budget"] -= 150
    elif effect_num == 5:
        effect_naam = "teleport naar start"
        posities[huidige]["x"] = 795
        posities[huidige]["y"] = 130
        posities[huidige]['straat'] = "geel"
    elif effect_num == 6:
        effect_naam = "ruil posities met tegenstander"
        temp_x = posities[tegenstander]["x"]
        temp_y = posities[tegenstander]["y"]

        posities[tegenstander]["x"] = posities[huidige]["x"]
        posities[tegenstander]["y"] = posities[huidige]["y"]

        posities[huidige]["x"] = temp_x
        posities[huidige]["y"] = temp_y
    elif effect_num == 7:
        aantal_eig = len(owned_pos_speler) if huidige == "speler" else len(owned_pos_bot)
        effect_naam = f"Krijg €{aantal_eig * 50} (€50 per eigendom)!"
        posities[huidige]["budget"] += aantal_eig*50
    elif effect_num == 8:
        aantal_eig = len(owned_pos_speler) if huidige == "speler" else len(owned_pos_bot)
        effect_naam = f"Betaal €{aantal_eig * 50} (€50 per eigendom)!"
        posities[huidige]["budget"] -= aantal_eig*50
    elif effect_num == 9:
        effect_naam = "spring 3 vakken terug"
        vakken_beweging -= 3
    elif effect_num == 10:
        effect_naam = "spring 3 vakken vooruit"
        vakken_beweging += 3
    print(f"Effect {effect_num}: {effect_naam}")
    bord.Screen.screen.blit(font.render(f"{huidige}: {effect_naam}", True, (255, 255, 0)), (200, 520))
    pygame.display.flip()
    pygame.time.wait(2000)
    
    return effect_num, effect_naam, vakken_beweging