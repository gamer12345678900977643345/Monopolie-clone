import pygame
import bord



# welke kleuren checken op welke as
AS_PER_KLEUR = {
    "rood":  "x",
    "blauw": "x",
    "geel":  "y",
    "groen": "y"
}

def toon_info(data, kleur, speler_pos_x, speler_pos_y, straat):
    if straat != kleur:
        return  # verkeerde straat → geen info tonen

    as_type = AS_PER_KLEUR[kleur]

    for vak in data[kleur]:
        if as_type == "x":
            positie_match = (speler_pos_x == vak["x"])
        else:
            positie_match = (speler_pos_y == vak["y"])

        if not positie_match:
            continue

        # teken vak
        pygame.draw.rect(bord.Screen.screen, (188, 180, 162), (900,200,300,240))
        pygame.draw.rect(bord.Screen.screen, (80,20,20),       (900,200,300,240), 5)

        # stats
        stats = [
            vak["naam"],
            f"Prijs: {vak['prijs']}",
            f"Huur: {vak['huur']}",
            f"Upgrade: {vak['upgrade']}",
            f"Eigenaar: {vak['eigenaar']}",
        ]

        for i, tekst in enumerate(stats):
            surface = font.render(tekst, True, (230,230,230))
            bord.Screen.screen.blit(surface, (910, 220 + i*40))

        # koop knop
        if vak["eigenaar"] is None:
            pygame.draw.rect(bord.Screen.screen, (200,200,100), (900,450,300,60))
            pygame.draw.rect(bord.Screen.screen, (80,20,20),     (900,450,300,60), 5)
            bord.Screen.screen.blit(font.render("Koop nu", True, (230,230,230)), (910,460))
