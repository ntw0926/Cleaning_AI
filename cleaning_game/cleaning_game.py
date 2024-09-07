import pygame
from enum import Enum
from pygame.locals import *
import numpy as np
    
class Roomba():
    size = pygame.Vector2(3,3)
    pos = pygame.Vector2(1,1)

    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

    def move(x, y):
        self.pos.x += x
        self.pos.y += y
        
class Map():
    map_tile = np.zeros((1,1))
    map_tile.astype(np.int32)

    def __init__(self, size:tuple):
        self.map_tile = np.zeros((size))
        self.map_tile.astype(np.int32)

    def set_loc_type(self, loc:tuple, tile_type:int):
        try:
            self.map_tile[loc[0]][loc[1]] = tile_type
        except:
            print("Set location " + str(loc) + " with tile type " + str(tile_type) + " failed")
    def get_map_tile(self):
        print(self.map_tile)


def base_game():
    pygame.display.set_caption("Roomba Game")
    map = Map((10,10))
