class Move:

    def __init__(self, src_pile, dest_pile):
        self.src_pile = src_pile
        self.dest_pile = dest_pile
        
        self.card = self.src_pile.top_card
    
    def __eq__(self, other):
        if type(self) != type(other):
            raise ValueError()

        return (type(self.src_pile) == type(other.src_pile) and
                type(self.dest_pile) == type(other.dest_pile) and
                self.card == other.card)

    def __str__(self):
        return ("Move(source: {}, dest: {}, card: {}").format(
                   type(self.src_pile).__name__, 
                   type(self.dest_pile).__name__, 
                   str(self.card)
               )

