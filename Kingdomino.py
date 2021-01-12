import pygame
from pygame.locals import *
from Engine import *
from Assets import Board
from KingdominoUI import *
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

    grid_length = len(e.get_player(e.get_players()[0]).get_board().get_grid())

    background = pygame.image.load('images/background.png')
    screen.blit(background, (0, 0))

    run = True
    while run:
        player_index = 0
        board_rects = []
        deal_rects = []
        for p in e.get_players():
            # kui.draw_board(screen, e.get_player(p).get_board(), player_index)
            grid_surf = pygame.Surface((TILE_SIZE*grid_length, TILE_SIZE*grid_length))
            grid_surf.set_alpha(255)
            draw_board(grid_surf, presets[player_index], player_index)
            board_rects.append(screen.blit(grid_surf, BOARD_OFFSET[player_index]))
            player_index += 1
        dom_number = 0
        for d in e.get_deal():
            deal_surf = pygame.Surface((TILE_SIZE*4, TILE_SIZE*2))
            draw_domino(deal_surf, d)
            deal_rects.append(screen.blit(deal_surf, (DEAL_OFFSET[0], DEAL_OFFSET[1] + dom_number*200)))
            dom_number += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if e.get_phase() == CLAIM:
                    for i in range(len(deal_rects)):
                        if deal_rects[i].collidepoint(pos):
                            e.claim_domino(e.get_current_player().get_name(), i)

        pygame.display.flip()
        clock.tick(fps)
