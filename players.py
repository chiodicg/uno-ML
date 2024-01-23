from cards import show_cards_list
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.playable_cards = []

    def __str__(self, ) -> str:
        return self.name

    def show_hand(self):
        return show_cards_list(self.hand)

    def add_to_hand(self, card):
        self.hand.append(card)

    def find_playable_card(self, card_on_pile):
        pile_colour = card_on_pile.colour
        pile_value = card_on_pile.value

        for card in self.hand:
            # Any wildcard, or Same coloured card (any value) or same valued card (any colour), including plus2
            if (card.colour == "wild" or card.colour == pile_colour or card.value == pile_value):
                self.playable_cards.append(str(card))
        # Sort playable cards
        self.playable_cards.sort(key=lambda card: str(card))
        
    def show_playable_cards(self):
        return show_cards_list(self.playable_cards)

