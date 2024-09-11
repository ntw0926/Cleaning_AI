from ai.Roomba_env import *
import pre_defined_maps

def main():
    pygame.init()
    screen = pygame.display.set_mode((1080,720))
    screen.fill("white")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont("malgungothic", 40)
    pygame.display.set_caption("Roomba Game")

    map = Map(pre_defined_maps.map_with_table)
    roomba = Roomba()
    env = Roomba_Base_Env()
    roomba.valid_movement(map, pygame.Vector2(0,0))
    map.draw_map(screen)
    roomba.draw_Roomba(screen)

    invalid_txt = font.render("Invalid used : " + str(env.invalid_used), False, (0,0,0))
    turn_txt = font.render("Turn used : " + str(env.turn_used), False, (0,0,0))
    move_txt = font.render("Move used : " + str(env.move_used), False, (0,0,0))
    screen.blit(invalid_txt, [650, 100])
    screen.blit(turn_txt, [650,200])
    screen.blit(move_txt, [650,300])

    cleaning_txt = font.render("Tiles " + str(map.clean_num) + " / " + str(map.all_num- map.unavailable_num), False, (0,0,0))
    screen.blit(cleaning_txt, [650, 400])
    pygame.display.flip()

    while running:
        update : action_type = action_type.Nan
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    update = roomba.action(map, direction.UP)
                    roomba.get_info()

                elif event.key == pygame.K_RIGHT:
                    update = roomba.action(map, direction.RIGHT)
                    roomba.get_info()

                elif event.key == pygame.K_DOWN:
                    update = roomba.action(map, direction.DOWN)
                    roomba.get_info()

                elif event.key == pygame.K_LEFT:
                    update = roomba.action(map, direction.LEFT)
                    roomba.get_info()

        if update != action_type.Nan:
            screen.fill("white")
            map.draw_map(screen)
            roomba.draw_Roomba(screen)

            env.invalid_used = (env.invalid_used + 1) if update == action_type.Invalid else (env.invalid_used)
            env.turn_used = (env.turn_used + 1) if update == action_type.Turn else (env.turn_used)
            env.move_used = (env.move_used + 1) if update == action_type.Move else (env.move_used)
            invalid_txt = font.render("Invalid used : " + str(env.invalid_used), False, ((200,0,0) if update == action_type.Invalid else (0,0,0)))
            turn_txt = font.render("Turn used : " + str(env.turn_used), False, ((200,0,0) if update == action_type.Turn else (0,0,0)))
            move_txt = font.render("Move used : " + str(env.move_used), False, ((200,0,0) if update == action_type.Move else (0,0,0)))

            if map.check_all_clean():
                cleaning_txt = font.render("Tiles " + str(map.clean_num) + " / " + str(map.all_num- map.unavailable_num), False, (200,0,0))
                screen.blit(font.render("Stage Cleared", False, (255,0,255)), [650,500])
                print("Stage Cleared")
                #time sleep 1
                #Reset map
                #Reset Roomba Posistion
                #Reset env to next session
            else:
                cleaning_txt = font.render("Tiles " + str(map.clean_num) + " / " + str(map.all_num- map.unavailable_num), False, (0,0,0))
            
            screen.blit(invalid_txt, [650, 100])
            screen.blit(turn_txt, [650,200])
            screen.blit(move_txt, [650,300])
            screen.blit(cleaning_txt, [650, 400])
            pygame.display.update()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()