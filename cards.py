import random

colours = ["red", "green", "blue", "yellow"]
wildcards = ["wild-colour", "wild-plus4"]

class Card:
    def __init__(self, colour, value):
        self.colour = colour
        self.value = value

    def show(self):
        return(self.colour + '_' + str(self.value))

class Deck:
    def __init__(self):
        self.cards = []
        self.cards_pile = []
        self.build()
        self.shuffle()

    def build(self):
        colours = ["red", "green", "blue", "yellow"]
        wildcards = ["colour", "plus4"]
        action = ["skip", "reverse", "plus2"]

        cards_zero = [Card(colour, 0) for colour in colours]
        cards_numbers = [Card(colour, value) for colour in colours for value in range(1,10)]*2
        cards_actions = [Card(colour, value) for colour in colours for value in action]*2
        cards_wildcards = [Card("wild", value) for value in wildcards]*4

        self.cards = cards_zero + cards_numbers + cards_actions + cards_wildcards
    
    def show(self):
        cards = []
        for card in self.cards:
            cards.append(card.show())
        return cards
    
    def length(self):
        return len(self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def discard(self, card):
        self.cards_pile.append(card)

    def show_last_discarded(self):
        self.cards_pile[-1].show()

    def show_discart_pile(self):
        for card in self.cards_pile:
            card.show()
    
    def draw_card(self):
        if len(self.cards) == 0:
            self.cards = self.cards_pile
            self.cards_disc = []
        return self.cards.pop()

    def flip_card(self):
        # Draw from deck and add to the discard pile
        while len(self.cards_pile) < 1 or self.cards_pile[-1].value not in range(0,10):
            self.cards_pile.append(self.draw_card())

    def deal_cards(self, players):
        for x in range(0,7):
            for player in list(players.keys()):
                players[player].add_to_hand(self.draw_card())