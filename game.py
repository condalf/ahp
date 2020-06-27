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
        possible_moves = self._get_possible_moves(current_player)

        while len(possible_moves) > 0:
            move = self._select_best_move(possible_moves)

            print(move)

            # Move the card between piles.
            card = move.src_pile.take()
            move.dest_pile.put(card)

            self._history.append(move)

            possible_moves = self._get_possible_moves(current_player)

    def _is_finished(self, current_player):
        return (len(self._get_near_left_pile(current_player)) == 0 and
                len(self._get_near_middle_pile(current_player)) == 0 and
                len(self._get_near_right_pile(current_player)) == 0)

    def _cannot_play(self, current_player):
        return len(self._get_possible_moves(current_player)) == 0

    def _get_next_player(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return Game.PLAYER_TWO
        else:
            return Game.PLAYER_ONE

    def _get_possible_moves(self, current_player):
        possible_moves = []

        src_piles = [self._get_near_left_pile(current_player),
                     self._get_near_middle_pile(current_player),
                     self._get_near_right_pile(current_player),
                     *self._outer_piles]

        for src_pile in src_piles:
            # Cannot move from an empty pile.
            if src_pile.is_empty():
                continue

            # Look for moves to the inner piles.
            for dest_pile in self._inner_piles:
                if dest_pile.accepts(src_pile.top_card):
                    possible_moves.append(Move(src_pile, dest_pile))

            # Look for moves to the outer piles
            for dest_pile in self._outer_piles:
                if dest_pile.accepts(src_pile.top_card):
                    possible_moves.append(Move(src_pile, dest_pile))

            # Look for moves onto the other player's piles.
            for dest_pile in [self._get_far_middle_pile(current_player),
                              self._get_far_left_pile(current_player)]:
                if dest_pile.accepts(src_pile.top_card):
                    possible_moves.append(Move(src_pile, dest_pile))

        return possible_moves

    def _select_best_move(self, possible_moves):
        # TODO Ban identical/reversed moves
        for move in possible_moves:
            # Check that this move is not the same as the last move
            if len(self._history) > 0 and move in self._history:
                continue

            # Check to see if moving the card will create a gap.
            if len(move.src_pile) == 1:
                return move

        # If nothing else works, use the first available move.
        # return possible_moves[0]
        return random.choice(possible_moves)

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

