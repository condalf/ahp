class CardPile:

    def __init__(self, cards):
        self._cards = cards

    def __iter__(self):
        return self._cards

    def __len__(self):
        return len(self._cards)
    

    def accepts(self, card):
        raise NotImplementedError()

    def is_empty(self):
        return len(self._cards) == 0

    def put(self, card):
        if self.accepts(card):
            self._cards.append(card)
        else:
            raise ValueError("card cannot be put on this pile")

    def take(self):
        return self._cards.pop()


    @property
    def top_card(self):
        if self.is_empty():
            return None
        else:
            return self._cards[-1]



class PlayerLeftPile(CardPile):

    def accepts(self, card):
        return (card.suit == self.top_card.suit and
                   (card.num == self.top_card.num+1 or
                    card.num == self.top_card.num-1))



class PlayerMiddlePile(CardPile):

    def __init__(self):
        """
        Construct the instance. No cards are required as input because the 
        pile always starts empty.
        """
        super().__init__([])


    def accepts(self, card):
        # Cards cannot be moved onto empty piles.
        if self.top_card == None:
            return False

        # The only valid move is for a card that is the next highest or
        # lowest and of the same suit.
        elif (card.suit == self.top_card.suit and 
                (card.num == self.top_card.num+1 or 
                    card.num == self.top_card.num-1)):
            return True

        else:
            return False



class PlayerRightPile(CardPile):

    def __init__(self, cards):
        super().__init__(cards)



class InnerPile(CardPile):

    def __init__(self):
        """
        Construct the instance. No cards are required as input because the 
        pile always starts empty.
        """
        super().__init__([])


    def accepts(self, card):
        # Only aces can start the inner piles.
        if self.is_empty():
            if card.name == "ace":
                return True
            else:
                return False

        # Cards can only be placed if they are the same suit and
        # are the next highest value.
        elif (card.suit == self.top_card.suit and 
               card.num == self.top_card.num+1):
            return True

        else: 
            return False

    def take(self, card):
        raise NotImplementedError()



class OuterPile(CardPile):

    def __init__(self, card):
        """
        Construct the instance. Only a single card is required as input because 
        the pile always starts with just one card in it.
        """
        super().__init__([card])


    def accepts(self, card):
        # Any card may move to empty piles
        if len(self._cards) == 0:
            return True

        # Otherwise the card must be the opposite color and the next
        # lowest value.
        elif (card.num == self.top_card.num-1 and 
                card.color != self.top_card.color):
            return True

        else:
            return False

