import pygame
from pygame.locals import *
from cleaning_game import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
                running = False
        base_game()
        screen.fill("purple")
        pygame.display.flip()

        clock.tick(60)


    pygame.quit()

if __name__ == "__main__":
    main()