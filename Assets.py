CASTLE = 'C'
WHEAT = 'W'
GRASS = 'G'
FOREST = 'F'
OCEAN = 'O'
SWAMP = 'S'
MINE = 'M'


class Board:
    def __init__(self):
        """Initializes the Board"""
        self._grid = [[None for i in range(9)] for j in range(9)]
        self._grid[4][4] = (CASTLE, 0)
        self._topmost = 4
        self._bottommost = 4
        self._leftmost = 4
        self._rightmost = 4

    def get_grid(self):
        """Returns the 2D list representation of the Board"""
        return self._grid

    def get_max_size(self):
        """Returns the maximum width of terrain-containing tiles"""
        return (len(self._grid) / 2) + 1

    def get_coord(self, row, col):
        """
        Returns the item at a particular coordinate, or None if the coordinates are out of bounds
        :param row: the row to check - cannot be negative
        :param col: the column to check - cannot be negative
        :return: the item at (row, col)
        """
        if 0 <= row < len(self._grid) and 0 <= col < len(self._grid[0]):
            return self._grid[row][col]
        else:
            return None
    
    def get_topmost(self):
        """Returns the lowest index row which contains an object"""
        return self._topmost
    
    def set_topmost(self, row):
        """
        Update the lowest index row which contains an object
        :param row: the index of the new topmost row
        """
        self._topmost = row

    def get_bottommost(self):
        """Returns the greatest index row which contains an object"""
        return self._bottommost

    def set_bottommost(self, row):
        """
        Update the greatest index row which contains an object
        :param row: the index of the new bottommost row
        """
        self._bottommost = row
        
    def get_leftmost(self):
        """Returns the lowest index column with contains an object"""
        return self._leftmost
    
    def set_leftmost(self, col):
        """
        Update the lowest index column which contains an object
        :param col: the index of the new leftmost column
        """
        self._leftmost = col

    def get_rightmost(self):
        """Returns the greatest index column with contains an object"""
        return self._rightmost

    def set_rightmost(self, col):
        """
        Update the greatest index column which contains an object
        :param col: the index of the new rightmost column
        """
        self._rightmost = col
    
    def check_match(self, row, col, a_terrain):
        """
        Checks if the terrain at a coordinate matches the parameter terrain
        :param row: the row number to check
        :param col: the column number to check
        :param a_terrain: a character representing the terrain
        :return: True if the terrain matches, False otherwise
        """
        terrain = self.get_coord(row, col)
        if terrain is None:
            return False
        else:
            return terrain[0] == a_terrain

    def check_match_castle(self, row, col, a_terrain):
        """
        Checks if the terrain at a coordinate matches the parameter terrain or is the castle
        :param row: the row number to check
        :param col: the column number to check
        :param a_terrain: a character representing the terrain
        :return: True if the terrain matches or is castle, False otherwise
        """
        terrain = self.get_coord(row, col)
        if terrain is None:
            return False
        else:
            return terrain[0] == a_terrain or terrain[0] == CASTLE

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


class Player:
    def __init__(self, name):
        self._name = name
        self._dom_on_hold = None
        self._board = Board()

    def get_name(self):
        return self._name

    def get_dom_on_hold(self):
        return self._dom_on_hold

    def set_dom_on_hold(self, domino):
        """
        Set the domino this player claimed but has not placed yet
        :param domino: a tuple of tuples representing a domino
        """
        self._dom_on_hold = domino

    def get_board(self):
        return self._board
