import pygame
from pygame.locals import *
from Engine import *
from KingdominoUI import *
import sys


player_names = sys.argv[1:]
# e = Engine(['blue', 'pink', 'yellow', 'green'])
e = Engine(player_names)

# presets = [Board(preset='sample_boards/exBoard{}.csv'.format(i+1)) for i in range(4)]

if not e.get_valid_setup():
    print('Invalid setup')
else:
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Kingdomino')
    sml_font = pygame.font.SysFont('arial', 20)
    font = pygame.font.SysFont('arial', 30)

    clock = pygame.time.Clock()
    fps = 12

    grid_length = len(e.get_player(e.get_players()[0]).get_board().get_grid())

    place_queue = [None for _ in range(len(e.get_players()))]

    run = True
    while run:
        background = pygame.image.load('images/background.png')
        screen.blit(background, (0, 0))
        logo = pygame.image.load('images/logo.png')
        screen.blit(logo, (685, 40))

        player_index = 0
        board_rects = [None for _ in range(len(e.get_players()))]
        deal_rects = [None for _ in range(len(e.get_players()))]
        discard_rects = [None for _ in range(len(e.get_players()))]
        # Draw the boards and player info
        for p in e.get_players():
            grid_surf = pygame.Surface((TILE_SIZE * grid_length, TILE_SIZE * grid_length))
            grid_surf.set_alpha(255)
            draw_board(grid_surf, e.get_player(p).get_board(), player_index)
            if place_queue[player_index] is not None:
                sel_row, sel_col = place_queue[player_index]
                selection = pygame.image.load('images/selection.png')
                grid_surf.blit(selection, (TILE_SIZE * sel_col, TILE_SIZE * sel_row))
            board_rects[player_index] = screen.blit(grid_surf, BOARD_OFFSET[player_index])
            # Display player name and score
            info = sml_font.render(p + '    Points: ' + str(e.get_player(p).get_score())
                                     + '    Crowns: ' + str(e.get_player(p).get_crowns()), True, (0, 0, 0))
            screen.blit(info, (BOARD_OFFSET[player_index][0], BOARD_OFFSET[player_index][1] + 460))
            # Draw a button for discarding during the placement phase
            if e.get_phase() == PLACE and e.get_player(p).get_dom_on_hold() is not None:
                discard_surf = pygame.image.load('images/discard_button.png')
                discard_rects[player_index] = screen.blit(discard_surf, (BOARD_OFFSET[player_index][0] + 370,
                                                                         BOARD_OFFSET[player_index][1] + 460))
            player_index += 1
        # Draw the deal and players who claimed each domino
        for i in range(len(e.get_deal())):
            deal_surf = pygame.Surface((TILE_SIZE*4, TILE_SIZE*2))
            draw_domino(deal_surf, e.get_deal()[i])
            deal_rects[i] = screen.blit(deal_surf, (DEAL_OFFSET[0], DEAL_OFFSET[1] + i * 150))
            if e.get_next_order()[i] is not None:
                text = font.render(e.get_next_order()[i].get_name(), True, (0, 0, 0))
                screen.blit(text, (DEAL_OFFSET[0] + 300, DEAL_OFFSET[1] + 20 + i * 150))
        # Update the status message
        message = None
        if not e.get_game_over():
            if e.get_phase() == CLAIM:
                message = font.render(e.get_current_player().get_name() + '\'s turn to choose.', True, (0, 0, 0))
            else:
                message = font.render('Place your dominoes', True, (0, 0, 0))
        else:
            message = font.render('Game Over!', True, (0, 0, 0))
        screen.blit(message, (DEAL_OFFSET[0], DEAL_OFFSET[1] + 600))

        # Add the Undo button
        if not e.get_game_over():
            undo_button = screen.blit(pygame.image.load('images/undo.png'), (910, 950))

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN and not e.get_game_over():
                pos = pygame.mouse.get_pos()
                if e.get_phase() == CLAIM:
                    for i in range(len(deal_rects)):
                        if deal_rects[i].collidepoint(pos):
                            e.claim_domino(e.get_current_player().get_name(), i)
                elif e.get_phase() == PLACE:
                    for i in range(len(board_rects)):
                        if board_rects[i].collidepoint(pos):
                            mouse_x, mouse_y = pos
                            offset_x, offset_y = BOARD_OFFSET[i]
                            row = (mouse_y - offset_y) // TILE_SIZE
                            col = (mouse_x - offset_x) // TILE_SIZE
                            if place_queue[i] is None:
                                place_queue[i] = (row, col)
                            else:
                                e.place_domino(e.get_players()[i], place_queue[i], (row, col))
                                place_queue[i] = None
                        if discard_rects[i] is not None:
                            if discard_rects[i].collidepoint(pos):
                                e.discard_domino(e.get_players()[i])
                if undo_button.collidepoint(pos):
                    e.undo()

        pygame.display.flip()
        clock.tick(fps)
