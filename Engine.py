from Assets import Board
import json
import random
from functools import cmp_to_key

P1 = 1
P2 = 2
P3 = 3
P4 = 4


class Engine:
    def __init__(self, players):
        self._valid_setup = False
        if 2 <= len(players) <= 4:
            self._valid_setup = True
            self._boards = [Board() for i in range(len(players))]
            self._deck = []
            self._turn = random.randint(P1,len(players))
            self._current_order = [0 for i in range(len(players))]
            self._next_order = [0 for i in range(len(players))]
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

    def deal_dominoes(self):
        """
        Deals a number of dominoes equal to the number of players
        :return: a list of dominoes sorted by number
        """
        deal = []
        if len(self._deck) >= len(self._boards):
            deal = self._deck[-len(self._boards):]
            self._deck = self._deck[:-len(self._boards)]
            deal = sorted(deal, key=lambda dom: dom[0])
            for d in deal:
                d = d[1:]
        return deal

    def claim_domino(self, player, position):
        pass

    def place_domino(self, player, coord1, coord2):
        pass

    def score_board(self, board):
        pass


e = Engine([0,0,0,0])
e.deal_dominoes()