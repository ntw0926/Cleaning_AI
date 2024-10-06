import sys
sys.path.append('d:\\Assignment\\graduate\\Cleaning_AI\\main_code')

from Ai.RoombaEnv import *
import Ai.BaseGame.PreDefinedMap as pre_defined_maps

#import roomba Ai variants
from Ai.AiExtentions.RoombaEnv_1Tile import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((1080,720))
    screen.fill("white")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("malgungothic", 40)
    pygame.display.set_caption("Roomba Game")

    dealt_map = Map(pre_defined_maps.basic_map)
    roomba = Roomba()
    env = RoombaEnv_1Tile(dealt_map,roomba)
    env.roomba.valid_movement(env.map, pygame.Vector2(0,0))
    env.map.draw_map(screen)
    env.roomba.draw_Roomba(screen)

    invalid_txt = font.render("Invalid used : " + str(env.invalid_used), False, (0,0,0))
    turn_txt = font.render("Turn used : " + str(env.turn_used), False, (0,0,0))
    move_txt = font.render("Move used : " + str(env.move_used), False, (0,0,0))
    screen.blit(invalid_txt, [650, 100])
    screen.blit(turn_txt, [650,200])
    screen.blit(move_txt, [650,300])

    cleaning_txt = font.render("Tiles " + str(env.map.clean_num) + " / " + str(env.map.all_num- env.map.unavailable_num), False, (0,0,0))
    screen.blit(cleaning_txt, [650, 400])
    pygame.display.flip()

    while running:
        if env.update != action_type.Nan:
            while env.step_lock:
                pass
            env.step_lock = True
            screen.fill("white")
            env.map.draw_map(screen)
            env.roomba.draw_Roomba(screen)
            invalid_txt = font.render("Invalid used : " + str(env.invalid_used), False, ((200,0,0) if update == action_type.Invalid else (0,0,0)))
            turn_txt = font.render("Turn used : " + str(env.turn_used), False, ((200,0,0) if update == action_type.Turn else (0,0,0)))
            move_txt = font.render("Move used : " + str(env.move_used), False, ((200,0,0) if update == action_type.Move else (0,0,0)))

            if env.map.check_all_clean():
                #visualization before reset
                screen.blit(invalid_txt, [650, 100])
                screen.blit(turn_txt, [650,200])
                screen.blit(move_txt, [650,300])
                screen.blit(cleaning_txt, [650, 400])
                screen.blit(font.render("Stage Cleared", False, (255,0,255)), [650,500])
                print("Stage Cleared")
                pygame.display.update()
                time.sleep(2)
                env.step_lock = False
                #reset
                while env.reset_lock:
                    pass
                env.roomba.valid_movement(env.map, pygame.Vector2(0,0))

                #visualization after reset
                screen.fill("white")
                env.map.draw_map(screen)
                env.roomba.draw_Roomba(screen)
                invalid_txt = font.render("Invalid used : " + str(env.invalid_used), False, (0,0,0))
                turn_txt = font.render("Turn used : " + str(env.turn_used), False, (0,0,0))
                move_txt = font.render("Move used : " + str(env.move_used), False, (0,0,0))
            
            cleaning_txt = font.render("Tiles " + str(env.map.clean_num) + " / " + str(env.map.all_num- env.map.unavailable_num), False, (0,0,0))
            screen.blit(invalid_txt, [650, 100])
            screen.blit(turn_txt, [650,200])
            screen.blit(move_txt, [650,300])
            screen.blit(cleaning_txt, [650, 400])
            pygame.display.update()
            env.update = action_type.Nan
            env.step_lock = False

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()