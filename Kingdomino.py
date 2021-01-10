import pygame
from pygame.locals import *
from Engine import Engine
from Assets import Board
import KingdominoUI as kui
import sys


player_names = sys.argv[1:]
e = Engine(['blue', 'pink', 'yellow', 'green'])

b1 = Board(preset='exBoard1.csv')

if not e.get_valid_setup():
    print('Invalid setup')
else:
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    run = True
    while run:
        background = pygame.image.load('images/background.png')
        screen.blit(background, (0,0))
        player_index = 0
        for p in e.get_players():
            kui.draw(b1, screen, player_index)
            player_index += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # handle position
        pygame.display.flip()