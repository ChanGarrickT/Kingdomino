import pygame
from pygame.locals import *

TILE_SIZE = 50

pygame.init()

screen = pygame.display.set_mode((1920,1080))

gameOn = True

while gameOn:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                gameOn = False
        elif event.type == QUIT:
            gameOn = False

    # Draw surface to location
    screen.blit(sq1.surf, (40,40))
    screen.blit(sq2.surf, (40,530))
    screen.blit(sq3.surf, (730,40))
    screen.blit(sq4.surf, (730, 530))

    pygame.display.flip()