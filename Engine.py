from Assets import Player
import json
import random
from functools import cmp_to_key

P1 = 0
P2 = 1
P3 = 2
P4 = 3
DEAL = 0
CLAIM = 1
PLACE = 2

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
                self._phase = DEAL
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
        return self._game_over

    def get_turn(self):
        return self._turn_order[self._turn]

    def get_player_count(self):
        return len(self._players)

    def deal_dominoes(self):
        """
        Deals a number of dominoes equal to the number of players
        :return: a list of dominoes sorted by number
        """
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
        try:
            player = self._players[name]
            if self._turn_order[self._turn] is player:
                if self._next_order[position] is None:
                    player.set_dom_on_hold(self._deal[position])
                    self._next_order[position] = player
                    self._turn += 1
                    print(name + ' claimed domino ' + str(self._deal[position]) + ' from slot ' + str(position + 1))
                else:
                    print('Domino already claimed.')
            else:
                print('Not ' + name + '\'s turn.')
        except KeyError:
            print('Name not found')

    def place_domino(self, player, coord1, coord2):
        pass

    def score_board(self, board):
        pass


e = Engine(['blue', 'pink'])
# game loop
e.deal_dominoes()
e.claim_domino('blue', 0)
e.claim_domino('pink', 1)
