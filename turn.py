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
    def __init__(self, player, deck, card_on_pile, game_over):
        self.player = player
        self.deck = deck
        self.card_on_pile = card_on_pile
        self.game_over = game_over
        self.find_playable()
        self.play()

    def __str__(self) -> str:
        pass

    def evaluate_table(self):
        # Evaluate if the card on the table is an action or wildcard
        if not self.card_on_pile.value.isdigit():
            if self.card_on_pile.value == 'plus4':
                pass
            if self.card_on_pile.value == 'colour':
                pass
            if self.card_on_pile.value == 'plus2':
                pass
            if self.card_on_pile.value == 'reverse':
                pass
            if self.card_on_pile.value == 'skip':
                pass


    def find_playable(self, hand=None):
        self.player.find_playable_card(self.card_on_pile, hand)

    def choose_card(self, list_of_playable):
        list_of_playable.sort(key=lambda card: sort_by_number(card))
        # This will remove from playable_cards list
        chosen_card = list_of_playable.pop(0)
        # Remove the card from hand list
        self.player.hand.remove(chosen_card)
        return chosen_card

    def play_card(self, chosen_card):
        # Add the card to the discard pile
        self.deck.add_to_discard(chosen_card)
        if (len(self.player.hand) == 0):
            self.game_over = True
            print(f'{str(self.player)} wins')

        # print(self.player.show_playable_cards(), self.player.show_hand())
        # print(str(chosen_card), self.deck.show_discard_pile())

    def play(self):
        # If player has a playable card, then choose one to discard
        print(f'{str(self.player)} has {len(self.player.playable_cards)} playable cards')
        print(f'{str(self.player)} has {len(self.player.hand)} in its hand')
        if (len(self.player.playable_cards) > 0):
            chosen_card = self.choose_card(self.player.playable_cards)
            self.play_card(chosen_card)
            print(f'{str(self.player)} plays the card {str(chosen_card)}')
        # Or draw a card
        else:
            print(f'{str(self.player)} is drawing a card')
            card_drawn = self.deck.draw_card()
            # evaluate card if playable
            if (self.player.is_playable(card_drawn, self.card_on_pile)):
                self.play_card(card_drawn)
                print(f'{str(self.player)} plays the card {str(card_drawn)}')
            else:
                # add card to hand and next turn
                self.player.hand.append(card_drawn)
                print(f'{str(self.player)} pass the turn')

    




