import pygame
from pygame.locals import *
from Engine import Engine
from Assets import Board
import KingdominoUI as kui
import sys


player_names = sys.argv[1:]
e = Engine(['blue', 'pink'])

b = Board(preset='exBoard1.csv')

if not e.get_valid_setup():
    print('Invalid setup')
else:
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # handle position
        kui.draw(b, screen, 0)
        pygame.display.flip()