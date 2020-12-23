CASTLE = 'C'
WHEAT = 'W'
GRASS = 'G'
FOREST = 'F'
OCEAN = 'O'
SWAMP = 'S'
MINE = 'M'


class Board:
    def __init__(self):
        self._grid = [[None for i in range(9)] for j in range(9)]
        self._grid[4][4] = (CASTLE, 0)

    def get_board(self):
        return self._grid

    def get_coord(self, row, col):
        return self._grid[row][col]

    def set_coord(self, row, col, obj):
        """
        Assigns an object to a grid tile
        :param row: the row number of the target tile
        :param col: the column number of the target tile
        :param obj: a tuple containing the terrain type, then the number of crowns
        """
        self._grid[row][col] = obj

    def print_board(self):
        row = 0
        for i in range(19):
            col = 0
            to_print = ''
            for j in range(19):
                if i % 2 == 0 and j % 2 == 0:
                    to_print += '+'
                elif i % 2 == 0:
                    to_print += '-----'
                elif j % 2 == 0:
                    to_print += '|'
                else:
                    if self._grid[row][col] is not None:
                        to_print += ' ' + self._grid[row][col][0] + ' ' + str(self._grid[row][col][1]) + ' '
                    else:
                        to_print += '     '
                    col += 1
            if i % 2 == 1:
                row += 1
            print(to_print)

b = Board()
b.print_board()