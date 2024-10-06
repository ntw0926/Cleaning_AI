import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')

from Ai.BaseGame.CleaningGame import *
import pyautogui
from gymnasium import Env
from gymnasium.spaces import Box, Discrete

#줄수있는 변수
#1. 총 활동 횟수 (무브, 턴, 인벨리드의 모든 액션의 합)
    #1-1. 각 무브에 따른 weight 부여
    #1-2. 총 활동수에만 가중치
    #1-3. 이동시 타일을 얼마나 치웠는지에 따른 weight 부여
    #1-4. 청소한 타일수 / 총 활동 횟수
#2. 주변 환경 (roomba가 차지하는 공간만, 혹은 roomba가 차지하는 공간에서 한칸씩 떨어져서 다음 이동할수 있는 공간 혹은 맵 전체)

class RoombaBaseEnv(Env):
    invalid_used : int
    move_used : int
    turn_used : int
    action_space : list
    map : Map = Map()
    roomba : Roomba = None

    update : action_type = action_type.Nan
    step_lock : bool = False
    reset_lock : bool = False
    prev_clean_num = 0


    def __init__(self,map : Map, roomba : Roomba):
        super().__init__()
        self.action_space = [direction.UP, direction.RIGHT, direction.DOWN, direction.LEFT]
        self.invalid_used = 0
        self.move_used = 0
        self.turn_used = 0
        if map:
            self.set_map(map)
        if roomba:
            self.roomba = roomba
            self.prev_clean_num = self.roomba.size.x * self.roomba.size.y

    def reset(self, seed=None):
        while self.reset_lock:
            pass
        self.reset_lock = True
        self.invalid_used = 0
        self.move_used = 0
        self.turn_used = 0
        self.map.reset_map()
        self.roomba.reset_pos()
        self.prev_clean_num = self.roomba.size.x * self.roomba.size.y
        self.update = action_type.Nan
        self.reset_lock = False
        return self.get_observation(), None

    def step(self, action:direction):
        while self.step_lock:
            pass
        self.step_lock = True
        if acion == direction.UP:
            update = self.roomba.action(self.map, direction.UP)
        elif action == direction.RIGHT:
            update = self.roomba.action(self.map, direction.RIGHT)
        elif action == direction.DOWN:
            update = self.roomba.action(self.map, direction.DOWN)
        elif action == direction.LEFT:
            update = self.roomba.action(self.map, direction.LEFT)
        else:
            update = action_type.Nan

        self.invalid_used = (self.invalid_used + 1) if update == action_type.Invalid else (self.invalid_used)
        self.turn_used = (self.turn_used + 1) if update == action_type.Turn else (self.turn_used)
        self.move_used = (self.move_used + 1) if update == action_type.Move else (self.move_used)

        return self.get_observation(), self.reward_function(), self.map.check_all_clean(), False, None

    def set_map(self, map:Map):
        self.map = map

    def get_observation(self):
        return None

    def reward_function(self, update : action_type) -> float:
        self.step_lock = False
        return 0.0