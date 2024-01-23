import random

class Card:
    def __init__(self, colour, value):
        self.colour = colour
        self.value = value

    def __str__(self) -> str:
        return self.colour + '_' + str(self.value)

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
        return show_cards_list(self.cards)
    
    def length(self):
        return len(self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def discard(self, card):
        self.cards_pile.append(card)

    def show_last_discarded(self):
        return str(self.cards_pile[-1])
    
    def get_last_discarded(self):
        return self.cards_pile[-1]

    def show_discard_pile(self):
        return show_cards_list(self.cards_pile)
    
    def draw_card(self):
        if len(self.cards) == 0:
            self.cards = random.shuffle(self.cards_pile)
            self.cards_disc = []
        return self.cards.pop()

    def flip_card(self):
        # Draw from deck and add to the discard pile
        while len(self.cards_pile) < 1 or self.cards_pile[-1].value not in range(0,10):
            self.add_to_discard(self.draw_card())

    def deal_cards(self, players):
        for x in range(0,7):
            for player in list(players.keys()):
                players[player].add_to_hand(self.draw_card())

    def add_to_discard(self, card):
        self.cards_pile.append(card)


def show_cards_list(list: list[Card]):
    cards = []
    for card in list:
        cards.append(str(card))
    return cards