import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')
import os
# Import Base Callback for saving models
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common import env_checker
from stable_baselines3.ppo import MultiInputPolicy
import tensorflow as tf

from Ai.RoombaEnv import *
import Ai.BaseGame.PreDefinedMap as pre_defined_maps

#import roomba Ai variants
import Ai.AiExtentions.RoombaEnv_1Tile as RE_1T
import Ai.AiExtentions.RoombaEnv_1Tile_TP as RE_1T_TP
import Ai.AiExtentions.RoombaEnv_1Tile_DR as RE_1T_DR
import Ai.AiExtentions.RoombaEnv_1Tile_DRTP as RE_1T_DRTP


class TrainAndLoggingCallback(BaseCallback):
    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)
        return True
    def _on_rollout_end(self):
        self.logger.record("Cleaned_tiles", self.training_env.get_attr("map")[0].clean_num)

map_text = "map_with_table"
model_text = "1Tile_Timepunishment"

CHECKPOINT_DIR = map_text + "/" + model_text + "/train"
LOG_DIR = map_text + "/" + model_text + "/log"


match map_text:
    case "map_basic":
        dealt_map = Map(pre_defined_maps.map_basic)
    case "map_with_mid_wall":
        dealt_map = Map(pre_defined_maps.map_with_mid_wall)
    case "map_with_side_wall":
        dealt_map = Map(pre_defined_maps.map_with_side_wall)
    case "map_with_table":
        dealt_map = Map(pre_defined_maps.map_with_table)
    case _:
        assert True

roomba = Roomba()

env = RE_1T.RoombaEnv_1Tile(dealt_map,roomba)
match map_text:
    case "1Tile":
        env = RE_1T.RoombaEnv_1Tile(dealt_map,roomba)
    case "1Tile_DirectionalReward":
        env = RE_1T_DR.RoombaEnv_1Tile_DirectionalReward(dealt_map,roomba)
    case "1Tile_Timepunishment":
        env = RE_1T_TP.RoombaEnv_1Tile_TimePunishment(dealt_map,roomba)
    case "1Tile_DirectionalRewardTimePunishment":
        env = RE_1T_DRTP.RoombaEnv_1Tile_DirectionalRewardTimePunishment(dealt_map,roomba)
    case _:
        assert True

env.unwrapped.map
env_checker.check_env(env)

def main():
    callback = TrainAndLoggingCallback(check_freq=100000, save_path=CHECKPOINT_DIR)
    model = PPO("MultiInputPolicy", env, tensorboard_log=LOG_DIR, verbose=1)
    model.learn(total_timesteps=10000000, callback=callback, progress_bar= True)

if __name__ == "__main__":
    main()