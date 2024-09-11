from base_game.cleaning_game import *
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

class Roomba_Base_Env(Env):
    invalid_used : int
    move_used : int
    turn_used : int
    cleaned_tiles : int
    action_space : list

    def __init__(self):
        super().__init__()
        self.reset()
        self.action_space = [direction.UP, direction.RIGHT, direction.DOWN, direction.LEFT]

    def reset(self, seed=None):
        self.invalid_used = 0
        self.move_used = 0
        self.turn_used = 0
        self.cleaned_tiles = 0

    def step(self, action:direction):
        if acion == direction.UP:
            pyautogui.press('up')
        elif action == direction.RIGHT:
            pyautogui.press('right')
        elif action == direction.DOWN:
            pyautogui.press('down')
        elif action == direction.LEFT:
            pyautogui.press('left')
        else:
            pass

    def reward_function(self) -> float:
        return 0.0

    def get_done(self):
        pass