from Assets import Player
import json
import random

P1 = 0
P2 = 1
P3 = 2
P4 = 3
CLAIM = 0
PLACE = 1


class Engine:
    def __init__(self, players, debug_mode=False):
        """
        Initializes the game
        :param players: A list of player names
        """
        self._valid_setup = False
        player_set = set(players)
        # Check for repeated player names
        if len(players) == len(player_set):
            # Check for valid number of players
            if 2 <= len(players) <= 4:
                self._valid_setup = True
                self._game_over = False
                self._players = {}
                for p in players:
                    self._players[p] = Player(p)
                self._phase = CLAIM
                self._deck = []
                self._turn_order = []
                for p in players:
                    self._turn_order.append(self._players[p])
                if not debug_mode:
                    random.shuffle(self._turn_order)
                self._turn = 0
                self._next_order = [None for i in range(len(players))]
                try:
                    with open('dominoes.json', 'r') as in_file:
                        data = json.load(in_file)
                        for d in data['dominoes']:
                            self._deck.append((d['number'], tuple(d['tile1']), tuple(d['tile2'])))
                    random.shuffle(self._deck)
                except FileNotFoundError:
                    print ('Domino data not found')
                self._deal = []
            else:
                print ('Invalid number of players')
        else:
            print('Player names not unique')

    def get_game_over(self):
        """Returns whether the game is over"""
        if not self._valid_setup:
            print('Invalid game setup')
            return
        return self._game_over

    def get_turn(self):
        """Returns the Player whose turn it is"""
        if not self._valid_setup:
            print('Invalid game setup')
            return
        return self._turn_order[self._turn]

    def get_player(self, name):
        """
        Returns a player instance given a name
        :param name: the name of the player to search for
        :return: the player instance, or None if name not found
        """
        if not self._valid_setup:
            print('Invalid game setup')
            return
        try:
            return self._players[name]
        except KeyError:
            print('Name not found')

    def get_player_count(self):
        """Returns the number of players in the game"""
        if not self._valid_setup:
            print('Invalid game setup')
            return
        return len(self._players)

    def deal_dominoes(self):
        """
        Deals a number of dominoes equal to the number of players
        :return: a list of dominoes sorted by number
        """
        if not self._valid_setup:
            print('Invalid game setup')
            return
        deal = []
        if len(self._deck) >= len(self._players):
            deal = self._deck[-len(self._players):]
            self._deck = self._deck[:-len(self._players)]
            deal = sorted(deal, key=lambda dom: dom[0])
            for d in deal:
                d = d[1:]
                self._deal.append(d)
                print(self._deal)
        return deal

    def claim_domino(self, name, position):
        """
        Claim a domino for a player
        :param name: name of the player who wishes to claim a domino
        :param position: the index of the domino to claim (lowest domino number is index 0)
        """
        if not self._valid_setup:
            print('Invalid game setup')
            return
        if self._phase != CLAIM:
            print('Not currently claim phase')
            return
        if self._next_order[position] is not None:
            print('Domino already claimed')
            return
        try:
            player = self._players[name]
            if self._turn_order[self._turn] is not player:
                print('Not ' + name + '\'s turn')
                return
            player.set_dom_on_hold(self._deal[position])
            self._next_order[position] = player
            self._turn += 1
            print(name + ' claimed domino ' + str(self._deal[position]) + ' from slot ' + str(position + 1))
            # Once all tiles are claimed, move to placement phase
            if self._turn >= len(self._players):
                self._turn = 0
                self._phase = PLACE
                print('Moving to Placement phase')
        except KeyError:
            print('Name not found')

    def place_domino(self, name, coord1, coord2):
        """
        Place a player's claimed domino on the board if possible
        :param name: the name of the player whose domino to place
        :param coord1: a tuple (row, col) representing where to place tile1 of the domino
        :param coord2: a tuple (row, col) representing where to place tile2 of the domino
        """
        if not self._valid_setup:
            print('Invalid game setup')
            return
        if self._phase != PLACE:
            print('Not currently Placement phase')
            return
        if not validate_coord(coord1, coord2):
            print('Invalid coordinates')
            return
        try:
            player = self._players[name]
            if player.get_dom_on_hold() is None:
                print(name + ' has no domino on hold')
                return
            if not validate_overlap(player.get_board(), coord1, coord2):
                print('One or more coordinates overlap with existing tile')
                return
            if not validate_neighbor(player.get_board(), player.get_dom_on_hold(), coord1, coord2):
                print('No matching adjacent tile')
                return
            max_size = player.get_board().get_max_size()
            size_updates = validate_size(player.get_board(), coord1, coord2, max_size)
            if not size_updates:
                print('Terrain grid cannot exceed ' + max_size + 'x' + max_size)
                return
            player.get_board().set_topmost(size_updates[0])
            player.get_board().set_bottommost(size_updates[1])
            player.get_board().set_leftmost(size_updates[2])
            player.get_board().set_rightmost(size_updates[3])
            player.get_board().set_coord(coord1[0], coord1[1], player.get_dom_on_hold()[0])
            player.get_board().set_coord(coord2[0], coord2[1], player.get_dom_on_hold()[1])
            print(name + ' placed ' + str(player.get_dom_on_hold()[0]) + ' at ' + str(coord1) +
                            ' and ' + str(player.get_dom_on_hold()[1]) + ' at ' + str(coord2))
            player.set_dom_on_hold(None)
            self._turn += 1
            if self._turn >= len(self._players):
                self._turn = 0
                self._phase = CLAIM
                print('Moving to Claim phase')
        except KeyError:
            print("Name not found")

    def discard_domino(self, name):
        if not self._valid_setup:
            print('Invalid game setup')
            return
        if self._phase != PLACE:
            print('Not currently Placement phase')
            return
        try:
            player = self._players[name]
            player.set_dom_on_hold(None)
            self._turn += 1
            if self._turn >= len(self._players):
                self._turn = 0
                self._phase = CLAIM
                print('Moving to Claim phase')
        except KeyError:
            print('Name not found')


def validate_coord(coord1, coord2):
    """
    Checks whether two coordinates are adjacent either horizontally or vertically
    :param coord1: a tuple (row, col) for the first coordinate
    :param coord2: a tuple (row, col) for the second coordinate
    :return: True if the coordinates are adjacent, False otherwise
    """
    dist_h = abs(coord1[0] - coord2[0])
    dist_v = abs(coord1[1] - coord2[1])
    if dist_h > 1 or dist_v > 1:
        return False
    elif dist_h + dist_v == 1:
        return True
    else:
        return False


def validate_overlap(board, coord1, coord2):
    """
    Checks whether the new domino would overlap with existing terrain
    :param board: the board to check
    :param coord1: a tuple (row, col) representing where to place tile1 of the domino
    :param coord2: a tuple (row, col) representing where to place tile2 of the domino
    :return: True if both coordinates are empty, False otherwise
    """
    x1, y1, x2, y2 = coord1[0], coord1[1], coord2[0], coord2[1]
    return board.get_coord(x1, y1) is None and board.get_coord(x2, y2) is None


def validate_neighbor(board, domino, coord1, coord2):
    """
    Checks whether a new domino would be adjacent to a matching terrain
    :param board: the board to check
    :param domino: a tuple of tuples representing the domino's tiles
    :param coord1: a tuple (row, col) representing where to place tile1 of the domino
    :param coord2: a tuple (row, col) representing where to place tile2 of the domino
    :return: True if the domino can be placed at the given coordinate, False if not
    """
    x1, y1, x2, y2 = coord1[0], coord1[1], coord2[0], coord2[1]
    terrain1 = domino[0][0]
    terrain2 = domino[1][0]
    validity1 = (board.check_match_castle(x1 - 1, y1, terrain1) or
                 board.check_match_castle(x1 + 1, y1, terrain1) or
                 board.check_match_castle(x1, y1 - 1, terrain1) or
                 board.check_match_castle(x1, y1 + 1, terrain1))
    validity2 = (board.check_match_castle(x2 - 1, y2, terrain2) or
                 board.check_match_castle(x2 + 1, y2, terrain2) or
                 board.check_match_castle(x2, y2 - 1, terrain2) or
                 board.check_match_castle(x2, y2 + 1, terrain2))
    return validity1 or validity2


def validate_size(board, coord1, coord2, max_size):
    """
    Checks whether placing the new domino would result in the board exceeding the maximum size
    :param board: the board to check
    :param coord1: a tuple (row, col) representing where to place tile1 of the domino
    :param coord2: a tuple (row, col) representing where to place tile2 of the domino
    :param max_size: the maximum number of tiles wide the board can be
    :return: a list of board bounds to update if the resulting board is within bounds, False otherwise
    """
    x1, y1, x2, y2 = coord1[0], coord1[1], coord2[0], coord2[1]
    topmost = min(board.get_topmost(), x1, x2)
    bottommost = max(board.get_bottommost(), x1, x2)
    leftmost = min(board.get_leftmost(), y1, y2)
    rightmost = max(board.get_rightmost(), y1, y2)
    if bottommost - topmost > max_size or rightmost - leftmost > max_size:
        return False
    else:
        return [topmost, bottommost, leftmost, rightmost]


def score_board(board):
    """
    Calculates and returns the score of the given board
    :param board: the board with which to calculate the score
    :return: the score
    """
    # Store all tiles to check in set
    unexplored = set()
    size = board.get_max_size()
    for i in range(size):
        for j in range(size):
            unexplored.add((i + board.get_topmost(), j + board.get_leftmost()))

    score = 0
    # While there are unexplored coordinates, find contiguous sections of terrain
    # Score per section is the product of its size and number of crowns
    while len(unexplored) > 0:
        section = _find_contiguous(board, unexplored.pop(), unexplored)
        unexplored -= section
        crowns = 0
        for c in section:
            crowns += board.get_coord(c[0], c[1])[1]
        score += (len(section) * crowns)
    return score


def _find_contiguous(board, coord, unexplored):
    row = coord[0]
    col = coord[1]
    if board.get_coord(row, col) is None:
        return set()
    # Make local copy of unexplored
    unexplored_copy = set(unexplored)
    # Add coord to contiguous
    contiguous = set()
    contiguous.add(coord)
    # For each unexplored neighbor with a matching terrain:
    #   Remove that neighbor from unexplored
    #   Recurse with each of those neighbors
    if board.get_coord(row - 1, col) is not None:
        if (row - 1, col) in unexplored_copy and board.get_coord(row, col)[0] == board.get_coord(row - 1, col)[0]:
            contiguous.update(_find_contiguous(board, (row - 1, col), unexplored_copy))
            unexplored_copy -= contiguous
    if board.get_coord(row + 1, col) is not None:
        if (row + 1, col) in unexplored_copy and board.get_coord(row, col)[0] == board.get_coord(row + 1, col)[0]:
            contiguous.update(_find_contiguous(board, (row + 1, col), unexplored_copy))
            unexplored_copy -= contiguous
    if board.get_coord(row, col - 1) is not None:
        if (row, col - 1) in unexplored_copy and board.get_coord(row, col)[0] == board.get_coord(row, col - 1)[0]:
            contiguous.update(_find_contiguous(board, (row, col - 1), unexplored_copy))
            unexplored_copy -= contiguous
    if board.get_coord(row, col + 1) is not None:
        if (row, col + 1) in unexplored_copy and board.get_coord(row, col)[0] == board.get_coord(row, col + 1)[0]:
            contiguous.update(_find_contiguous(board, (row, col + 1), unexplored_copy))
            unexplored_copy -= contiguous

    return contiguous


e = Engine(['blue', 'pink'], True)
# game loop
e.deal_dominoes()
e.claim_domino('blue', 0)
e.claim_domino('pink', 1)
e.place_domino('blue', (3,4), (3,5))
e.get_player('blue').get_board().print_board()
print(score_board(e.get_player('blue').get_board()))
e.place_domino('pink', (4,5), (4,6))
e.get_player('pink').get_board().print_board()
print(score_board(e.get_player('pink').get_board()))

