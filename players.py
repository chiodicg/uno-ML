class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def show_name(self):
        return self.name

    def show_hand(self):
        cards = []
        for card in self.hand:
            cards.append(card.show())
        return cards

    def add_to_hand(self, card):
        self.hand.append(card)