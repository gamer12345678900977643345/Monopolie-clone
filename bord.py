import pygame

class Screen:
    breedte = 1280
    hoogte = 720
    screen = pygame.display.set_mode((breedte, hoogte), pygame.RESIZABLE)
    pygame.display.set_caption("Moneypoly")
#dit mag wrs weg
class Tile:
    tile_x_rel = 0.5
    tile_y_rel = 0.5    
    tile_button_w_rel = 0.20     
    tile_button_h_rel = 0.20    
    tile_rect = pygame.Rect(
        int(Screen.breedte * tile_x_rel),
        int(Screen.hoogte * tile_y_rel),
        int(Screen.breedte * tile_button_w_rel),
        int(Screen.hoogte * tile_button_h_rel)
    )

    #flip functie in de main.py houden
    
tiles = pygame.draw.rect(Screen.screen, (255,255,255), Tile.tile_rect)
tile_pos = [(int(160*i)+50, int(i)+400) for i in range(4)]

#print(f"tiles: {tiles}")    

