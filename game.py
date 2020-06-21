from card import make_deck


class Move:

    def __init__(self, src_pile, dest_pile):
        self.src_pile = src_pile
        self.dest_pile = dest_pile


class Game:

    PLAYER_ONE = 1
    PLAYER_TWO = 2


    def __init__(self):
        left_piles = []
        right_piles = []
        outer_piles = []
        for player in [Game.PLAYER_ONE,Game.PLAYER_TWO]:
            left_pile,starter_cards,right_pile = self._init_player(player)
            left_piles.append(left_pile)
            right_piles.append(right_pile)
            for card in starter_cards:
                outer_piles.append([card])

        self._left_piles = left_piles
        self._middle_piles = [[],[]]
        self._right_piles = right_piles
        self._inner_piles = [[] for _ in range(8)]  # 8 empty lists
        self._outer_piles = outer_piles


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

            # Move the card between piles.
            card = move.src_pile.pop()
            move.dest_pile.append(card)

            possible_moves = self._get_possible_moves(current_player)

    def _is_finished(self, current_player):
        return (len(self._get_near_left_pile(current_player)) == 0 and
                len(self._get_near_middle_pile(current_player)) == 0 and
                len(self._get_near_right_pile(current_player)) == 0)

    def _cannot_play(self, current_player):
        return len(self.get_possible_moves(current_player)) == 0

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
            if len(src_pile) == 0:
                continue

            src_card = src_pile[-1]

            # Look for moves to the inner piles.
            for dest_pile in self._inner_piles:
                # Only aces can start the inner piles.
                if len(dest_pile) == 0:
                    if src_card.name == "ace":
                        possible_moves.append(Move(src_pile, dest_pile))
                    continue

                dest_card = dest_pile[-1]

                # Cards can only be placed if they are the same suit and
                # are the next highest value.
                if (src_card.suit == dest_card.suit and
                        src_card.num == dest_card.num + 1):
                    possible_moves.append(Move(src_pile, dest_pile))

            # Look for moves to the outer piles
            for dest_pile in self._outer_piles:
                # Any card may move to empty piles
                if len(dest_pile) == 0:
                    possible_moves.append(Move(src_pile, dest_pile))
                    continue

                dest_card = dest_pile[-1]

                # Otherwise the card must be the opposite color and the next
                # lowest value.
                if (src_card.num == dest_card.num - 1 and 
                        src_card.color != dest_card.color):
                    possible_moves.append(Move(src_pile, dest_pile))

            # Look for moves onto the other player's piles.
            for dest_pile in [self._get_far_middle_pile(current_player),
                              self._get_far_right_pile(current_player)]:
                # Cards cannot be moved onto empty piles.
                if len(dest_pile) == 0:
                    continue

                dest_card = dest_pile[-1]

                # The only valid move is for a card that is the next highest or
                # lowest and of the same suit.
                if (src_card.suit == dest_card.suit and
                        (src_card.num == dest_card.num + 1 or
                         src_card.num == dest_card.num - 1)):
                    possible_moves.append(Move(src_pile, dest_pile))

        return possible_moves

    def _select_best_move(self, possible_moves):
        for move in possible_moves:
            # Check to see if moving the card will create a gap.
            if len(move.src_pile) == 1:
                return move

        # If nothing else works, use the first available move.
        return possible_moves[0]

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

    def _get_far_middle_pile(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return self._middle_piles[1]
        else:
            return self._middle_piles[0]

    def _get_far_right_pile(self, current_player):
        if current_player == Game.PLAYER_ONE:
            return self._right_piles[1]
        else:
            return self._right_piles[0]

