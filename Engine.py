from Assets import Player
import json
import random
from copy import deepcopy

P1 = 0
P2 = 1
P3 = 2
P4 = 3
CLAIM = 0
PLACE = 1


class Engine:
    def __init__(self, players):
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
        """
        Returns whether the game is over
        :return: True if all tiles have been claimed
        """
        if not self._valid_setup:
            print('Invalid game setup')
            return
        return self._game_over

    def get_turn(self):
        """
        Returns the Player whose turn it is
        :return: the Player
        """
        if not self._valid_setup:
            print('Invalid game setup')
            return
        return self._turn_order[self._turn]

    def get_player_count(self):
        """
        Returns the number of players in the game
        :return: the number of players
        """
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
            if self._turn == len(self._players):
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
            print('Not currently place phase')
            return
        if not validate_coord(coord1, coord2):
            print('Invalid coordinates')
            return
        try:
            player = self._players[name]
        except KeyError:
            print("Name not found")

    def validate_placement(self, name, coord1, coord2):
        dup_board = deepcopy(self._players[name].get_board())
        domino = self._players[name].get_dom_on_hold()
        tile1 = domino[0]
        tile2 = domino[1]


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


def score_board(board):
    pass


e = Engine(['blue', 'pink'])
# game loop
e.deal_dominoes()
e.claim_domino('blue', 0)
e.claim_domino('pink', 1)
