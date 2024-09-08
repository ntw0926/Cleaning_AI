import pygame
from pygame.locals import *
from cleaning_game import *
import pre_defined_maps

def main():
    pygame.init()
    screen = pygame.display.set_mode((720,720))
    screen.fill("white")
    clock = pygame.time.Clock()
    running = True
    
    pygame.display.set_caption("Roomba Game")
    map = Map(pre_defined_maps.map_with_table)
    roomba = Roomba()
    roomba.valid_movement(map, pygame.Vector2(0,0))
    map.draw_map(screen)
    roomba.draw_Roomba(screen)
    pygame.display.flip()
    while running:
        update = False
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
        if update:
            map.draw_map(screen)
            roomba.draw_Roomba(screen)
            pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()