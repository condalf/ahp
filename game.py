import random

from card import make_deck
from cardpile import (PlayerLeftPile, 
                      PlayerMiddlePile,
                      PlayerRightPile,
                      InnerPile,
                      OuterPile)
from move import Move


class Game:

    PLAYER_ONE = 1
    PLAYER_TWO = 2


    def __init__(self):
        left_piles = []
        middle_piles = []
        right_piles = []
        inner_piles = []
        outer_piles = []

        for player in [Game.PLAYER_ONE,Game.PLAYER_TWO]:
            left_pile,starter_cards,right_pile = self._init_player(player)

            left_piles.append(PlayerLeftPile(left_pile))
            middle_piles.append(PlayerMiddlePile())
            right_piles.append(PlayerRightPile(right_pile))

            for _ in range(4):
                inner_piles.append(InnerPile())

            for card in starter_cards:
                outer_piles.append(OuterPile(card))

        self._left_piles = left_piles
        self._middle_piles = middle_piles
        self._right_piles = right_piles
        self._inner_piles = inner_piles
        self._outer_piles = outer_piles

        self._history = []


    def play(self):
        current_player = self._get_starting_player()
        while True:
            self._take_turn(current_player)

            if self._is_finished(current_player):
                print("Success! Player {} wins!".format(current_player))
                break
            elif (self._cannot_play(Game.PLAYER_ONE) and 
                    self._cannot_play(Game.PLAYER_TWO)):
                print("Failure. No moves are possible.")
                break
            else:
                current_player = self._get_next_player(current_player)


    def _init_player(self, player):
        deck = make_deck()

        left_pile = []
        for _ in range(13):
            left_pile.append(deck.pop())

        starter_cards = []
        for _ in range(4):
            starter_cards.append(deck.pop())

        return left_pile,starter_cards,deck

    def _get_starting_player(self):
        # TODO Add appropriate logic
        return Game.PLAYER_ONE

    def _take_turn(self, current_player):
        move = self._select_best_move(current_player)
        while move is not None:

            print(move)

            # Move the card between piles.
            card = move.src_pile.take()
            move.dest_pile.put(card)

            move = self._select_best_move(current_player)

    def _is_finished(self, current_player):
        return (len(self._get_near_left_pile(current_player)) == 0 and
                len(self._get_near_middle_pile(current_player)) == 0 and
                len(self._get_near_right_pile(current_player)) == 0)

    def _cannot_play(self, current_player):
        # TODO Add appropriate logic.
        return False

    def _get_next_player(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return Game.PLAYER_TWO
        else:
            return Game.PLAYER_ONE

    def _select_best_move(self, current_player):
        # Check for aces.
        for pile in [self._get_near_left_pile(current_player),
                     self._get_near_middle_pile(current_player),
                     self._get_near_right_pile(current_player),
                     *self._outer_piles]:
            if pile.is_empty(): continue

            if pile.top_card.name == "ace":
                for inner_pile in self._inner_piles:
                    if inner_pile.is_empty():
                        return Move(pile, inner_pile)

        # Check for twos.
        for pile in [self._get_near_left_pile(current_player),
                     self._get_near_middle_pile(current_player),
                     self._get_near_right_pile(current_player),
                     *self._outer_piles]:
            if pile.is_empty(): continue

            if pile.top_card.num == 2:
                for inner_pile in self._inner_piles:
                    if inner_pile.accepts(pile.top_card):
                        return Move(pile, inner_pile)

        # Can I make a gap by manipulating the outer piles?
        # Can I increase outer pile sizes?
        # Can I make a gap by moving onto the inner piles?
        # What can I do with my personal cards (from either L, M or R)?
            # Put on outer piles? (not a gap)
            # Put in middle?
            # Put on opponent?

    def _get_near_left_pile(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return self._left_piles[0]
        else:
            return self._left_piles[1]

    def _get_near_middle_pile(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return self._middle_piles[0]
        else:
            return self._middle_piles[1]

    def _get_near_right_pile(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return self._right_piles[0]
        else:
            return self._right_piles[1]

    def _get_far_left_pile(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return self._left_piles[1]
        else:
            return self._left_piles[0]

    def _get_far_middle_pile(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return self._middle_piles[1]
        else:
            return self._middle_piles[0]

