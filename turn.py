""" Put playable cards in order:
1. Highest numbered cards
2. Action cards (plus 2, skip, reverse)
3. Wildcards
 """
def sort_by_number(card):
        if (not str(card).startswith('wild')):
            if(str(card).split("_")[-1].isdigit()):
                return f"0{str(card)}"
            else:
                return f"1{str(card)}"
        else:
            return f"2{str(card)}"
        

"""
Each turn:
Players will play the cards in turns, one card at a time. Card must match colour, number or symbol
You may pickup a new card from the deck if you don't want to play or can't
If the card you pickup is the only playable card which you have then you can play it
"""
class Turn:
    def __init__(self, player, deck, card_on_pile):
        self.player = player
        self.deck = deck
        self.card_on_pile = card_on_pile
        self.find_playable()
        self.play()

    def __str__(self) -> str:
        pass

    def find_playable(self):
        self.player.find_playable_card(self.card_on_pile)

    def choose_card(self, list_of_playable):
        print('before sorting', list_of_playable)
        list_of_playable.sort(key=lambda card: sort_by_number(card))
        print('after sorting', list_of_playable)
        # This will remove from playable_cards list
        return list_of_playable.pop()

    def play_card(self, chosen_card):
        # Remove the card from hand list
        self.player.hand.remove(chosen_card)
        # Add the card to the discard pile
        self.deck.add_to_discard(chosen_card)
        
        print(self.player.show_playable_cards(), self.player.show_hand())
        print(str(chosen_card), self.deck.show_discard_pile())

    def play(self):
        # If player has a playable card, then choose one to discard
        print(len(self.player.playable_cards))
        if (len(self.player.playable_cards) > 0):
            chosen_card = self.choose_card(self.player.playable_cards)
            self.play_card(chosen_card)
        # Or draw a card
        else:
            # draw card
            # evaluate card if playable
            # if not, pass;
            # if yes, play;
            pass

    




