import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')

from Ai.BaseGame.CleaningGame import *
from gymnasium import *
from gymnasium.spaces import Space, Discrete

#줄수있는 변수
#1. 총 활동 횟수 (무브, 턴, 인벨리드의 모든 액션의 합)
    #1-1. 각 무브에 따른 weight 부여
    #1-2. 총 활동수에만 가중치
    #1-3. 이동시 타일을 얼마나 치웠는지에 따른 weight 부여
    #1-4. 청소한 타일수 / 총 활동 횟수
#2. 주변 환경 (roomba가 차지하는 공간만, 혹은 roomba가 차지하는 공간에서 한칸씩 떨어져서 다음 이동할수 있는 공간 혹은 맵 전체)
    #2-1 Roomba의 위치에 1칸씩을 추가한 사각형
    #2-2 map에서 남은 dirty tile의 위치들
    #2-3 map 전체
#3. roomba의 위치와 direction

class RoombaBaseEnv(Env):
    invalid_used : int
    move_used : int
    turn_used : int
    action_space : list
    map : Map = Map()
    roomba : Roomba = None
    is_first_display = True

    #For step and reward
    update : action_type = action_type.Nan
    prev_clean_num = 0
    step_taken = 0

    #For displaying
    font = None
    screen = None
    clock = None

    def __init__(self,map : Map, roomba : Roomba):
        super().__init__()
        self.action_space = Discrete(4)
        if map:
            self.set_map(map)
        if roomba:
            self.roomba = roomba
            self.roomba.valid_movement(self.map, pygame.Vector2(0,0))
            self.prev_clean_num = self.map.clean_num
        self.invalid_used = 0
        self.move_used = 0
        self.turn_used = 0
        if self.screen == None:
            pygame.init()
            self.screen = pygame.display.set_mode((1080,720))
            self.screen.fill("white")
            self.clock = pygame.time.Clock()
        
            self.font = pygame.font.SysFont("malgungothic", 40)
            pygame.display.set_caption("Roomba Game")
            pygame.display.update()

    def _get_info(self):
        return{
            "invalid use" : self.invalid_used,
            "move use" : self.move_used,
            "turn use" : self.turn_used,
            "roomba pos" : self.roomba.pos,
            "roomba dir" : self.roomba.arrow
        }

    def reset(self, seed = None, options = None):
        if self.screen != None and not self.is_first_display:
            #visualization before reset
            invalid_txt = self.font.render("Invalid used : " + str(self.invalid_used), False, ((200,0,0) if self.update == action_type.Invalid else (0,0,0)))
            turn_txt = self.font.render("Turn used : " + str(self.turn_used), False, ((200,0,0) if self.update == action_type.Turn else (0,0,0)))
            move_txt = self.font.render("Move used : " + str(self.move_used), False, ((200,0,0) if self.update == action_type.Move else (0,0,0)))         
            cleaning_txt = self.font.render("Tiles " + str(self.map.clean_num) + " / " + str(self.map.all_num- self.map.unavailable_num), False, (0,0,0))
            self.screen.blit(invalid_txt, [650, 100])
            self.screen.blit(turn_txt, [650,200])
            self.screen.blit(move_txt, [650,300])
            self.screen.blit(cleaning_txt, [650, 400])
            self.screen.blit(self.font.render("Stage Cleared", False, (255,0,255)), [650,500])
            print("Stage Cleared")
            pygame.display.update()

        super().reset(seed=seed)
        self.invalid_used = 0
        self.move_used = 0
        self.turn_used = 0
        self.map.reset_map()
        self.roomba.reset_pos()
        self.roomba.valid_movement(self.map, pygame.Vector2(0,0))
        self.prev_clean_num = self.map.clean_num
        self.update = action_type.Nan
        self.step_taken = 0
        return self.get_observation(), self._get_info()

    def step(self, action):
        self.step_taken += 1
        action_map = {
        0:direction.UP,
        1:direction.RIGHT,
        2:direction.DOWN,
        3:direction.LEFT
        }
        if action == 0:
            self.update = self.roomba.action(self.map, direction.UP)
        elif action == 1:
            self.update = self.roomba.action(self.map, direction.RIGHT)
        elif action == 2:
            self.update = self.roomba.action(self.map, direction.DOWN)
        elif action == 3:
            self.update = self.roomba.action(self.map, direction.LEFT)
        else:
            assert("unexpected behavior in step")
            update = action_type.Nan

        self.invalid_used = (self.invalid_used + 1) if self.update == action_type.Invalid else (self.invalid_used)
        self.turn_used = (self.turn_used + 1) if self.update == action_type.Turn else (self.turn_used)
        self.move_used = (self.move_used + 1) if self.update == action_type.Move else (self.move_used)

        self.render()

        return self.get_observation(), self.reward_function(), self.map.check_all_clean(), (self.step_taken >= 1000), self._get_info()

    def set_map(self, map:Map):
        self.map = map

    def get_observation(self):
        return None

    def reward_function(self) -> float:
        assert("Reward function is Empty")
        return 0.0

    def render(self):
        pygame.event.clear()
        self.screen.fill("white")
        self.map.draw_map(self.screen)
        self.roomba.draw_Roomba(self.screen)
        invalid_txt = self.font.render("Invalid used : " + str(self.invalid_used), False, ((200,0,0) if self.update == action_type.Invalid else (0,0,0)))
        turn_txt = self.font.render("Turn used : " + str(self.turn_used), False, ((200,0,0) if self.update == action_type.Turn else (0,0,0)))
        move_txt = self.font.render("Move used : " + str(self.move_used), False, ((200,0,0) if self.update == action_type.Move else (0,0,0)))         
        cleaning_txt = self.font.render("Tiles " + str(self.map.clean_num) + " / " + str(self.map.all_num- self.map.unavailable_num), False, (0,0,0))
        self.screen.blit(invalid_txt, [650, 100])
        self.screen.blit(turn_txt, [650,200])
        self.screen.blit(move_txt, [650,300])
        self.screen.blit(cleaning_txt, [650, 400])
        pygame.display.update()
        self.clock.tick(0)
    
    def close(self):
        if self.screen != None:
            pygame.display.quit()
            pygame.quit()