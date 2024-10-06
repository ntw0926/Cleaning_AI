import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')
import os
# Import Base Callback for saving models
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3.common import env_checker

CHECKPOINT_DIR = './train/'
LOG_DIR = './logs/'

from Ai.RoombaEnv import *
import Ai.BaseGame.PreDefinedMap as pre_defined_maps

#import roomba Ai variants
from Ai.AiExtentions.RoombaEnv_1Tile import *


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


def main():
    dealt_map = Map(pre_defined_maps.basic_map)
    roomba = Roomba()
    env = RoombaEnv_1Tile(dealt_map,roomba)
    env_checker.check_env(env)
    callback = TrainAndLoggingCallback(check_freq=10000, save_path=CHECKPOINT_DIR)
    model = DQN('MlpPolicy', env, tensorboard_log=LOG_DIR, verbose=1, buffer_size=120000, learning_starts=5, learning_rate = 0.01)
    model.learn(total_timesteps=500000, callback=callback)

if __name__ == "__main__":
    main()