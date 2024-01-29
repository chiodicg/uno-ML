from cards import show_cards_list
from actions import draw_cards
import random

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
        self.game_over = False
        print(f'The card on the table is {str(self.card_on_pile)}. It is {str(self.player)} turn.')
        self.find_playable()
        self.play()
        self.shout = False

    def __str__(self) -> str:
        if self.game_over:
            return f'Game over. {str(self.player)} wins!'
        else:
            return 'Game still ongoing'
        
    def shout_UNO_choice(self):
        shout_choice = input('Do you want to shout UNO? Please reply with "Yes" or "No". ').lower()
        if shout_choice == 'yes' or shout_choice == 'y':
            print(f'{str(self.player)} shouts UNO!')
            self.shout = True
            return True
        elif shout_choice == 'random' or shout_choice == '':
            rand_shout = random.choice([True, False])
            self.shout = rand_shout
            return rand_shout
        else:
            self.shout = False
            return False

    def evaluate_hand(self):
        # To implement later if we want the option to shout UNO at any part of the play
        # if len(self.player.hand) > 1:
        #     if self.shout:
        #         draw_cards(self.deck, 2, self.player)
        #         self.shout = False
        if len(self.player.hand) == 1:
            shout = self.shout_UNO_choice()
            if not shout:
                draw_cards(self.deck, 2, self.player)
            else:
                self.shout = False
        elif len(self.player.hand) == 0:
            self.game_over = True

    def find_playable(self, hand=None):
        self.player.find_playable_card(self.card_on_pile, hand)

    def validate_chosen(self, chosen_card):
        list_strings = show_cards_list(self.player.playable_cards)
        
        # if index not present on list
        if chosen_card.isdigit():
            if not int(chosen_card) in range(0, len(self.player.playable_cards)):
                return False
            else:
                return int(chosen_card)
        # if card does not exist on list
        else:
            if chosen_card == '':
                return 0
            elif chosen_card == 'random':
                return random.randint(0, len(list_strings)-1)
            elif not chosen_card in list_strings:
                return False
            else:
                return list_strings.index(chosen_card)
            
    def choice_for_card(self):
        chosen_card = input(f'Choose one of the playable cards by typing "random" OR the index (from 0 to {str(len(self.player.playable_cards)-1)}) OR the name of the card: ')
        return self.validate_chosen(chosen_card)

    def choose_card(self):
        self.player.playable_cards.sort(key=lambda card: sort_by_number(card))
        print(f'This is the list of {str(self.player)} playable cards: {self.player.show_playable_cards()}')
        chosen = self.choice_for_card()
        while chosen is False:
            chosen = self.choice_for_card()
        # This will remove from playable_cards list
        get_card = self.player.playable_cards.pop(chosen)
        print(f'{str(self.player)} played {str(get_card)}')
        # Remove the card from hand list
        self.player.hand.remove(get_card)
        return get_card

    def play_card(self, chosen_card):
        # Add the card to the discard pile
        self.deck.discard(chosen_card)
        print(f'{str(self.player)} plays the card {str(chosen_card)}')
        # self.shout_UNO_choice()

    def play(self):
        # If player has a playable card, then choose one to discard
        print(f'{str(self.player)} has {len(self.player.playable_cards)} playable cards')
        if (len(self.player.playable_cards) > 0):
            chosen_card = self.choose_card()
            self.play_card(chosen_card)
        # Or draw a card
        else:
            print(f'{str(self.player)} is drawing a card')
            card_drawn = self.deck.draw_card()
            # evaluate card if playable
            if (self.player.is_playable(card_drawn, self.card_on_pile)):
                self.play_card(card_drawn)
            else:
                # add card to hand and next turn
                self.player.hand.append(card_drawn)
                print(f'{str(self.player)} pass the turn')
        self.evaluate_hand()
        print(f'{str(self.player)} has {len(self.player.hand)} in its hand')

    




