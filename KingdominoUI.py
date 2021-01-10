import pygame
from pygame.locals import *
from Assets import Board


TILE_SIZE = 50
CROWN_SIZE = 15
BOARD_OFFSET = [(60,60), (1410,60), (60,570), (1410,570)]
TERRAINS = {'W': 'wheat.png', 'F': 'forest.png', 'O': 'ocean.png', 'G': 'grass.png', 'S': 'swamp.png', 'M': 'mine.png'}
CASTLES = ['castle_blue.png', 'castle_pink.png', 'castle_yellow.png', 'castle_green.png']


def draw(board, surface, player_number):
    for row in range(len(board.get_grid())):
        for col in range(len(board.get_grid()[0])):
            tile = board.get_coord(row, col)
            tile_img = ''
            if tile is not None:
                if tile[0] == 'C':
                    tile_img = pygame.image.load('images/' + CASTLES[0])
                else:
                    tile_img = pygame.image.load('images/' + TERRAINS[tile[0]])
                x = BOARD_OFFSET[player_number][0] + col * TILE_SIZE
                y = BOARD_OFFSET[player_number][1] + row * TILE_SIZE
                surface.blit(tile_img, (x, y))


