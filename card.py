import random


class Card:

    SUITS = ["clubs","diamonds","hearts","spades"]


    def __init__(self, num, suit):
        self.num = num
        self.suit = suit
        self.name = self._get_name(num)
        self.color = self._get_suit_color(suit)

    def __eq__(self, other):
        if type(self) != type(other):
            raise ValueError()

        return self.num == other.num and self.suit == other.suit

    def __str__(self):
        return "{} of {}".format(self.name, self.suit)


    def _get_name(self, num):
        if num == 1:
            return "ace"
        elif num == "11":
            return "jack"
        elif num == "12":
            return "queen"
        elif num == "13":
            return "king"
        else:
            return str(num)

    def _get_suit_color(self, suit):
        if suit == "clubs" or suit == "spades":
            return "black"
        else:
            return "red"


def make_deck():
    cards = []
    for suit in Card.SUITS:
        for num in range(1, 14):
            cards.append(Card(num, suit))
    random.shuffle(cards)
    return cards

