import random

colours = ["red", "green", "blue", "yellow"]

class Card:
    def __init__(self, colour, value, score):
        self.colour = colour
        self.value = value
        self.score = score

    def __str__(self) -> str:
        return self.colour + '_' + str(self.value)

class Deck:
    def __init__(self):
        self.cards = []
        self.cards_pile = []
        self.build()
        self.shuffle()

    def build(self):
        wildcards = ["colour", "plus4"]
        action = ["skip", "reverse", "plus2"]

        cards_zero = [Card(colour, 0, 0) for colour in colours]
        cards_numbers = [Card(colour, value, value) for colour in colours for value in range(1,10)]*2
        cards_actions = [Card(colour, value, 25) for colour in colours for value in action]*2
        cards_wildcards = [Card("wild", value, 50) for value in wildcards]*4

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
            # Remove any cards with None value (when players would play the Colour Wildcard and choose a new colour)
            self.cards_pile = list(filter(lambda card: card.value != None, self.cards_pile))
            # Keep the last discarded card, shuffle the rest of the pile to make them as a deck
            last_card = self.cards_pile.pop(-1)
            random.shuffle(self.cards_pile)
            self.cards = self.cards_pile
            self.cards_pile = [last_card]
        return self.cards.pop(0)

    def flip_card(self):
        # Draw from deck and add to the discard pile
        while len(self.cards_pile) < 1 or self.cards_pile[-1].value not in range(0,10):
            self.discard(self.draw_card())

    def deal_cards(self, list_of_players):
        for x in range(0,7):
            for player in list_of_players:
                player.add_to_hand(self.draw_card())

def show_cards_list(list: list[Card]):
    cards = []
    for card in list:
        cards.append(str(card))
    return cards