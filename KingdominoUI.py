import pygame
from pygame.locals import *
from Assets import Board


TILE_SIZE = 50
CROWN_SIZE = 15
BOARD_OFFSET = [(60, 60), (1410, 60), (60, 570), (1410, 570)]
DEAL_OFFSET = (785, 190)
TERRAINS = {'W': 'wheat.png', 'F': 'forest.png', 'O': 'ocean.png', 'G': 'grass.png', 'S': 'swamp.png', 'M': 'mine.png'}
CASTLES = ['castle_blue.png', 'castle_pink.png', 'castle_yellow.png', 'castle_green.png']


def draw_board(surface, board, player_number):
    x = y = 0
    for row in range(len(board.get_grid())):
        for col in range(len(board.get_grid()[0])):
            tile = board.get_coord(row, col)
            tile_img = ''
            if tile is not None:
                if tile[0] == 'C':
                    tile_img = pygame.image.load('images/' + CASTLES[player_number])
                else:
                    tile_img = pygame.image.load('images/' + TERRAINS[tile[0]])
                x = BOARD_OFFSET[player_number][0] + col * TILE_SIZE
                y = BOARD_OFFSET[player_number][1] + row * TILE_SIZE

                surface.blit(tile_img, (x, y))
                crown_pos = x
                for _ in range(tile[1]):
                    surface.blit(pygame.image.load('images/crown.png'), (crown_pos, y))
                    crown_pos += CROWN_SIZE
    return pygame.Rect(x, y, TILE_SIZE * len(board.get_grid()[0]), TILE_SIZE * len(board.get_grid()))


def draw_deal(surface, dominoes):
    x, y = DEAL_OFFSET
    for d in dominoes:
        tile_img = pygame.image.load('images/' + TERRAINS[d[0][0]])
        tile_img = pygame.transform.scale(tile_img, (100, 100))
        surface.blit(tile_img, (x, y))
        x2 = x + TILE_SIZE * 2
        tile_img = pygame.image.load('images/' + TERRAINS[d[1][0]])
        tile_img = pygame.transform.scale(tile_img, (100, 100))
        surface.blit(tile_img, (x2, y))
        y += 200


def draw_tile():
    pass


def draw_claims(surface, claims):
    pass
