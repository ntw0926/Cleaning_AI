import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')

from Ai.RoombaEnv import *

class RoombaEnv_1Tile_Timepunishment(RoombaBaseEnv):
    def __init__(self,map : Map, roomba : Roomba):
        super().__init__(map, roomba)
        obs_map = spaces.Box(low= 0, high=2, shape=(int(self.roomba.size.x +2), int(self.roomba.size.y + 2)), dtype=np.int64)
        roomba_pos = spaces.Box(low = 0, high = max(self.map.map_tile.shape[0], self.map.map_tile.shape[1]), shape=[2], dtype=np.int64)
        self.observation_space = spaces.Dict({"Roomba_dir" :spaces.Discrete(4), "Roomba_pos": roomba_pos, "Space": obs_map})

    #override
    #Observe one tile bigger square from Roomba 
    def get_observation(self):
        obs_map = np.zeros((int(self.roomba.size.x + 2), int(self.roomba.size.y + 2)), dtype=np.int64)
        for i in range(int(self.roomba.pos.x - 1), int(self.roomba.pos.x + self.roomba.size.x)):
            for j in range(int(self.roomba.pos.y - 1), int(self.roomba.pos.y + self.roomba.size.y)):
                obs_map[i - int(self.roomba.pos.x) + 1][j - int(self.roomba.pos.y) + 1] = self.map.map_tile[i][j]
        roomba_pos = np.array([np.int64(self.roomba.pos.x), np.int64(self.roomba.pos.y)])
        roomba_dir = np.int64(self.roomba.arrow.value)
        return {"Roomba_dir" : roomba_dir, "Roomba_pos" : roomba_pos,  "Space" : obs_map}

    #override
    #Invalid move will get punishment
    #turn will not grant any reward nor punishment
    #move will grant reward based on number of tiles cleaned on that move
    # There is reward time factor that will punish when time goes by
    def reward_function(self) -> float:
        reward : float = -self.step_taken/10.0
        if self.update == action_type.Invalid:
            return reward - 10
        elif self.update == action_type.Turn:
            return reward
        elif self.update == action_type.Move:
            cleaned_this_move = self.map.clean_num - self.prev_clean_num
            self.prev_clean_num = self.map.clean_num
            return reward + (cleaned_this_move * 100)
        elif self.update == action_type.Nan:
            assert("unexpected behavior in reward_function")
            return 0
        else:
            assert("update has no attribute of action type")
            return 0
        assert("Reward function unexpected happens with update " + str(self.update))
        return -1