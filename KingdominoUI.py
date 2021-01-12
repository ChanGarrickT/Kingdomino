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
    for row in range(len(board.get_grid())):
        for col in range(len(board.get_grid()[0])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = board.get_coord(row, col)
            if tile is not None:
                draw_tile(surface, tile, x, y, castle_color=('images/' + CASTLES[player_number]))


def draw_domino(surface, domino):
    draw_tile(surface, domino[0], 0, 0, 100)
    draw_tile(surface, domino[1], 100, 0, 100)


def draw_tile(surface, tile, x, y, size=TILE_SIZE, castle_color=None):
    """
    Draw a domino tile at (0, 0)
    :param surface: the surface on which to draw
    :param tile: a tuple representing terrain and number of crowns
    :param x: the x coordinate at which to draw the tile
    :param y: the y coordinate at which to draw the tile
    :param size: the size at which to draw the tile
    :param castle_color: the path of the image for drawing a castle
    :return: a PyGame Surface holding this tile
    """
    tile_img = None
    if tile[0] == 'C':
        tile_img = pygame.image.load(castle_color)
    else:
        tile_img = pygame.image.load('images/' + TERRAINS[tile[0]])

    crown_pos = 0
    for _ in range(tile[1]):
        tile_img.blit(pygame.image.load('images/crown.png'), (crown_pos, 0))
        crown_pos += CROWN_SIZE

    tile_img = pygame.transform.scale(tile_img, (size, size))
    surface.blit(tile_img, (x, y))


def draw_claims(surface, claims):
    pass
