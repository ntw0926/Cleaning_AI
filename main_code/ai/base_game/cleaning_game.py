import pygame
from enum import Enum, unique, global_enum
from pygame.locals import *
import numpy as np
import time

@unique
@global_enum
class direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

@unique
class tile(Enum):
    Unavailable = 0
    Dirty = 1
    Clean = 2

@unique
class action_type(Enum):
    Nan = -1
    Invalid = 0
    Move = 1
    Turn = 2

#The Map we are going to clean
class Map():
    map_tile : np.array
    all_num : int
    clean_num : int
    unavailable_num : int

    def __init__(self, array : np.array = np.ones((10,10))):
        self.map_tile = array
        self.map_tile.astype(np.int32)
        self.all_num = self.map_tile.size
        print(self.all_num)
        self.clean_num = 0

        it = np.nditer(self.map_tile, flags = ['multi_index'])
        self.unavailable_num = 0
        while not it.finished:
            idx = it.multi_index
            if self.map_tile[idx] == tile.Unavailable.value:
                self.unavailable_num += 1
            it.iternext()
        print(self.unavailable_num)


    def check_all_clean(self) -> bool :
        if self.all_num == self.unavailable_num + self.clean_num:
            return True
        return False

    def set_map_tile_type(self, loc:tuple, tile_type:tile):
        try:
            self.map_tile[loc[0]][loc[1]] = tile_type.value
        except:
            print("Set location " + str(loc) + " with tile type " + str(tile_type) + " failed")
            pygame.quit()

    def get_map_tile(self):
        print(self.map_tile)

    def clean_tiles(self, clean_pos: list):
        for loc in clean_pos:
            if self.map_tile[loc[0]][loc[1]] == tile.Dirty.value:
                self.clean_num += 1
                self.set_map_tile_type(loc, tile.Clean)

    def draw_map(self, surface : pygame.Surface):
        it = np.nditer(self.map_tile, flags = ['multi_index'])
        while not it.finished:
            idx = it.multi_index
            rect = pygame.Rect(idx[0]*50, idx[1]*50,50,50)
            color = (255,255,255)
            if self.map_tile[idx] == tile.Unavailable.value:
                color = (0,0,0)
            elif self.map_tile[idx] == tile.Dirty.value:
                color = (120,120,0)
            elif self.map_tile[idx] == tile.Clean.value:
                color = (0, 120, 120)
            else:
                print("Unknown type of tile" + str(self.map_tilep[idx]))
                pygame.quit()
                break
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, "black", rect, 1)
            it.iternext()


#Roomba the Vacuum machine
class Roomba():
    size : pygame.Vector2
    #Position of Left bottom 
    pos : pygame.Vector2
    arrow = direction.UP
    
    def __init__(self, size:pygame.Vector2 = pygame.Vector2(2,2), pos:pygame.Vector2 = pygame.Vector2(1,1)):
        self.size = size
        self.pos = pos

    def valid_movement(self, map : Map, movement : pygame.Vector2) -> action_type:
        if movement.x != 0 and movement.y !=0:
            print("Can't move Diagnoally")
            return action_type.Invalid

        temp_pos = self.pos + movement
        clean_arr = []
        if temp_pos.x < 0 or temp_pos.x + self.size.x > map.map_tile.shape[0]:
            print("Roomba out of Map")
            return action_type.Invalid
        if  temp_pos.y < 0 or temp_pos.y + self.size.y > map.map_tile.shape[1]:
            print("Roomba out of Map")
            return action_type.Invalid

        i = 0
        for i in range(int(self.size.x)):
            j=0
            for j in range(int(self.size.y)):
                search_tile_x = int(temp_pos.x) + i
                search_tile_y = int(temp_pos.y) + j
                if map.map_tile[search_tile_x][search_tile_y] == tile.Unavailable.value:
                    print("Roomba enter invalid part of Map")
                    clean_arr.clear()
                    return action_type.Invalid
                clean_arr.append((search_tile_x, search_tile_y))

        self.pos = temp_pos
        map.clean_tiles(clean_arr)
        return action_type.Move
        

    def move(self, map : Map, amount : int) -> action_type:
        match self.arrow:
            case direction.UP:
                return self.valid_movement(map, pygame.Vector2(0,-1))
            case direction.RIGHT:
                return self.valid_movement(map, pygame.Vector2(1,0))
            case direction.DOWN:
                return self.valid_movement(map, pygame.Vector2(0,1))
            case direction.LEFT:
                return self.valid_movement(map, pygame.Vector2(-1,0))
            case _:
                print("Arrow Exception with arrow = " + self.arrow)
                pygame.quit()
                return action_type.Invalid

    def turn(self, clockwise:bool):
        val_temp = self.arrow.value
        if clockwise:
            val_temp = (val_temp + 1) % 4
        else :
            val_temp = (val_temp + 3) % 4
        self.arrow = direction(val_temp)

    def action(self, map : Map, key_press : direction) -> action_type:
        if self.arrow == key_press:
            return self.move(map,1)
        elif (self.arrow.value + 1)%4 == key_press.value:
            self.turn(True)
            return action_type.Turn
        elif (self.arrow.value + 3)%4 == key_press.value:
            self.turn(False)
            return action_type.Turn
        else:
            print("invalid movement")
            return action_type.Invalid

    def get_info(self):
        print("Roomba at " + str(self.pos))
        print("Roomba facing " + str(self.arrow))

    def draw_Roomba(self, surface:pygame.Surface):
        rect = pygame.Rect(int(self.pos[0])*50, int(self.pos[1])*50, int(self.size[0])*50, int(self.size[1])*50)
        pygame.draw.rect(surface, (100,100,100) , rect, 0, 15)
        triangle = [[0,0],[0,0],[0,0]]

        if self.arrow == direction.UP:
            top_mid = [self.pos[0]*50+self.size[0]*25 , self.pos[1]*50 + 10]
            left = [top_mid[0] - 10, top_mid[1] + 10]
            right = [top_mid[0] + 10, top_mid[1] + 10]
            triangle = [top_mid, left, right]

        elif self.arrow == direction.RIGHT:
            right_mid = [self.pos[0]*50 + self.size[0]*50 - 10 , self.pos[1]*50 + self.size[1] * 25]
            top = [right_mid[0] - 10, right_mid[1] - 10]
            bottom = [right_mid[0] - 10, right_mid[1] + 10]
            triangle = [right_mid, top, bottom]

        elif self.arrow == direction.DOWN:
            bottom_mid = [self.pos[0]*50+self.size[0]*25 , self.pos[1]*50 + self.size[1]*50 - 10]
            left = [bottom_mid[0] - 10, bottom_mid[1] - 10]
            right = [bottom_mid[0] + 10, bottom_mid[1] - 10]
            triangle = [bottom_mid, left, right]

        elif self.arrow == direction.LEFT:
            left_mid = [self.pos[0]*50+10 , self.pos[1]*50 + self.size[1] * 25]
            top = [left_mid[0] + 10, left_mid[1] - 10]
            bottom = [left_mid[0] + 10, left_mid[1] + 10]
            triangle = [left_mid, top, bottom]
        pygame.draw.polygon(surface, "red", triangle, 0)