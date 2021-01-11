import pygame
from pygame.locals import *
from Engine import Engine
from Assets import Board
import KingdominoUI as kui
import sys


player_names = sys.argv[1:]
e = Engine(['blue', 'pink', 'yellow', 'green'])

presets = [Board(preset='sample_boards/exBoard{}.csv'.format(i+1)) for i in range(4)]

if not e.get_valid_setup():
    print('Invalid setup')
else:
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

    clock = pygame.time.Clock()
    fps = 12

    run = True
    while run:
        background = pygame.image.load('images/background.png')
        screen.blit(background, (0,0))
        player_index = 0
        for p in e.get_players():
            # kui.draw_board(screen, e.get_player(p).get_board(), player_index)
            kui.draw_board(screen, presets[player_index], player_index)
            player_index += 1
        kui.draw_deal(screen, e.get_deal())
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # handle position

        pygame.display.flip()
        clock.tick(fps)
