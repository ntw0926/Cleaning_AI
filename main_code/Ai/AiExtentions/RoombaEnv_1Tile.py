import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')

from Ai.RoombaEnv import *

class RoombaEnv_1Tile(RoombaBaseEnv):
    def __init__(self,map : Map, roomba : Roomba):
        super().__init__()

    #override
    #Observe one tile bigger square from Roomba
    def get_observation(self):
        obs_map = np.array.zeros((self.roomba.size.x + 2, self.roomba.size.y + 2 )) 
        for i in range(self.roomba.pos.x - 1, self.roomba.pos.x + self.roomba.size.x):
            for j in range(self.roomba.pos.y - 1, self.roomba.pos.y + self.roomba.size.y):
                obs_map[i - self.roomba.pos.x + 1][j - self.roomba.pos.y + 1] = self.map[i][j]
        print(obs_map.size())
        return obs_map

    #override
    #Invalid move will get punishment
    #turn will not grant any reward nor punishment
    #move will grant reward based on number of tiles cleaned on that move
    # Important : We don't have time factor, so it will take forever to clean the tiles
    def reward_function(self) -> float:
        if self.update == action_type.Invalid:
            self.step_lock = False
            return -10
        elif self.update == action_type.Turn:
            self.step_lock = False
            return 0
        elif self.update == action_type.Move:
            cleaned_this_move = self.map.clean_num - self.prev_clean_num
            self.prev_clean_num = self.map.clean_num
            self.step_lock = False
            return cleaned_this_move * 10
        elif self.update == action_type.Nan:
            self.step_lock = False
            return 0
        self.step_lock = False
        assert("Reward function unexpected happens with update " + str(self.update))
        return -1