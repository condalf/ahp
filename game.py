import random

SUITS = ["clubs","diamonds","hearts","spades"]

class Card:
    def __init__(self, num, suit):
        if num == 1:
            self.name = "ace"
        else:
            self.name = str(num)

        self.num = num
        self.suit = suit

        if suit == "clubs" or suit == "spades":
            self.color = "black"
        else:
            self.color = "red"

    def __str__(self):
        return "{} {}".format(self.num, self.suit)

def make_deck():
    cards = []
    for suit in SUITS:
        for num in range(1, 14):
            cards.append(Card(num, suit))
    random.shuffle(cards)
    return cards

def print_cards(cards):
    for card in cards:
        print(card)

class Game:
    def __init__(self):
        self.asc_piles = []
        self.desc_piles = []

        for _ in range(8):
            self.asc_piles.append([])
            self.desc_piles.append([])

        deck1 = make_deck()
        deck2 = make_deck()

        self.player1_left_pile = deck1[:13]

        self.desc_piles[0].append(deck1[13])
        self.desc_piles[1].append(deck1[14])
        self.desc_piles[2].append(deck1[15])
        self.desc_piles[3].append(deck1[16])

        self.player1_middle_pile = []
        self.player1_right_pile = deck1[17:]

        self.player2_left_pile = deck2[:13]

        self.desc_piles[4].append(deck2[13])
        self.desc_piles[5].append(deck2[14])
        self.desc_piles[6].append(deck2[15])
        self.desc_piles[7].append(deck2[16])

        self.player2_middle_pile = []
        self.player2_right_pile = deck2[17:]

    def play(self):
        current_player = 1

        while True:
            self.make_moves(current_player)

            if self.player_is_out(current_player):
                print("SUCCESS")
                return
            elif self.is_stuck(1) and self.is_stuck(2):
                print("STUCK")
                return
            else:
                if current_player == 1:
                    current_player = 2
                else:
                    current_player = 1

    def player_is_out(self, player):
        if player == 1:
            if (len(self.player1_left_pile) == 0 and
               len(self.player1_middle_pile) == 0 and
               len(self.player1_right_pile) == 0):
                    return True   
        else:
            if (len(self.player2_left_pile) == 0 and
               len(self.player2_middle_pile) == 0 and
               len(self.player2_right_pile) == 0):
                    return True   
        return False

    def is_stuck(self, player):
        if len(self.get_possible_moves(player)) == 0:
            return True
        else:
            return False

    def make_moves(self, player):
        possible_moves = self.get_possible_moves(player)

        while len(possible_moves) > 0:
            src,dest = self.select_best_move(possible_moves)

            card = src.pop()
            dest.append(card)

            possible_moves = self.get_possible_moves(player)

    def select_best_move(self, possible_moves):
        for move in possible_moves:
            src,dest = move

            if len(src) == 1:
                return move
        return possible_moves[0]

    def get_possible_moves(self, player):
        possible_moves = []

        srcs = self.desc_piles
        other_player_piles = []

        if player == 1:
            srcs.append(self.player1_left_pile)
            srcs.append(self.player1_middle_pile)
            srcs.append(self.player1_right_pile)

            other_player_piles.append(self.player2_left_pile)
            other_player_piles.append(self.player2_middle_pile)
        else:
            srcs.append(self.player2_left_pile)
            srcs.append(self.player2_middle_pile)
            srcs.append(self.player2_right_pile)

            other_player_piles.append(self.player1_left_pile)
            other_player_piles.append(self.player1_middle_pile)

        for src in srcs:
            if len(src) == 0: continue

            src_card = src[len(src)-1]

            for dest in self.asc_piles:
                if len(dest) == 0:
                    if src_card.name == "ace":
                        move = src,dest
                        possible_moves.append(move)
                    continue

                dest_card = dest[len(dest)-1]
                if (src_card.suit == dest_card.suit and
                        src_card.num == dest_card.num + 1):
                    move = src,dest
                    possible_moves.append(move)

            for dest in self.desc_piles:
                if len(dest) == 0:
                    move = src,dest
                    possible_moves.append(move)
                else:
                    dest_card = dest[len(dest)-1]
                    if (src_card.num == dest_card.num - 1 and 
                            src_card.color != dest_card.color):
                        move = src,dest
                        possible_moves.append(move)

            for dest in other_player_piles:
                if len(dest) == 0:
                    continue

                dest_card = dest[len(dest)-1]
                if (src_card.suit == dest_card.suit and
                        (src_card.num == dest_card.num + 1 or
                         src_card.num == dest_card.num - 1)):
                    move = src,dest
                    possible_moves.append(move)
        return possible_moves

