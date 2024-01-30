from cards import Card, show_cards_list
        
class Player:
    def __init__(self, name, bot):
        self.name = name
        self.bot = bot
        self.hand = []
        self.playable_cards = []

    def __str__(self, ) -> str:
        return self.name

    def show_hand(self):
        return show_cards_list(self.hand)

    def add_to_hand(self, card):
        if isinstance(card, Card):
            self.hand.append(card)
        else:
            self.hand.extend(card)

    def find_playable_card(self, card_on_pile):
        self.playable_cards = []

        for card in self.hand:
            # Any wildcard, or Same coloured card (any value) or same valued card (any colour), including plus2
            if (self.is_playable(card, card_on_pile)):
                self.playable_cards.append(card)
        
    def show_playable_cards(self):
        return show_cards_list(self.playable_cards)
    
    def is_playable(self, card, card_on_pile):
        return card.colour == "wild" or card.colour == card_on_pile.colour or card.value == card_on_pile.value


    