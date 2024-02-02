from cards import show_cards_list, Card
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
                return f"2{str(card)}"
            else:
                return f"1{str(card)}"
        else:
            return f"0{str(card)}"
        

"""
Each turn:
Players will play the cards in turns, one card at a time. Card must match colour, number or symbol
You may pickup a new card from the deck if you don't want to play or can't
If the card you pickup is the only playable card which you have then you can play it
"""
class Turn:
    def __init__(self, player, deck):
        self.player = player
        self.deck = deck
        self.card_on_pile = deck.get_last_discarded()
        self.game_over = False
        self.chosen_card = None
        print(f'The card on the table is {str(self.card_on_pile)}. It is {str(self.player)} turn.')
        self.find_playable()
        print(f'{str(self.player)} has {len(self.player.playable_cards)} playable cards')
        self.same_colour = [card for card in self.player.playable_cards if card.colour == self.card_on_pile.colour]
        self.same_value = [card for card in self.player.playable_cards if card.value == self.card_on_pile.value]
        self.wildcard = [card for card in self.player.playable_cards if card.colour == "wild"]
        
    def shout_UNO_choice(self):
        shout_choice = input('Do you want to shout UNO? Please reply with "Yes" or "No". ').lower()
        if shout_choice == 'yes' or shout_choice == 'y':
            return True
        elif shout_choice == 'random' or shout_choice == '':
            rand_shout = random.choice([True, False])
            return rand_shout
        else:
            return False
    
    def turn_message(self):
        if self.game_over:
            return f'Game over. {str(self.player)} wins!'
        else:
            return f'{str(self.player)} played {str(self.chosen_card)}. Game still ongoing'

    def evaluate_hand(self):
        # To implement later if we want the option to shout UNO at any part of the play
        # if len(self.player.hand) > 1:
        #     if self.shout:
        #         draw_cards(self.deck, 2, self.player)
        #         self.shout = False
        if len(self.player.hand) == 1:
            if self.player.bot:
                shout = random.choice([True, False])
            else:
                shout = self.shout_UNO_choice()

            if not shout:
                draw_cards(self.deck, 2, self.player)
            else:
                print(f'{str(self.player)} shouts UNO!')
        elif len(self.player.hand) == 0:
            self.game_over = True
        print(f'{str(self.player)} has {len(self.player.hand)} in its hand')

    def find_playable(self):
        self.player.find_playable_card(self.card_on_pile)
        self.player.playable_cards.sort(key=lambda card: sort_by_number(card), reverse=True)

    def get_card(self, chosen_method):
        choices = {
            'colour': self.same_colour,
            'value': self.same_value,
            'wildcard': self.wildcard
        }

        if chosen_method == 'colour' or chosen_method == 'value' or chosen_method == 'wildcard':
            return choices[chosen_method][0]
        elif chosen_method == 'bot':
            return self.player.playable_cards[0]
        else:
            return self.player.playable_cards[random.randint(0, len(self.player.playable_cards)-1)]
            
    def choice_for_card(self):
        if self.player.bot:
            return self.player.playable_cards[0]
        else:
            methods = ''
            if len(self.same_colour) > 0:
                methods = methods + 'colour or '
            if len(self.same_value) > 0:
                methods = methods + 'value or '
            if len(self.wildcard) > 0:
                methods = methods + 'wildcard or '
            methods = methods + 'random'

            chosen_method = input(f'Do you want to choose a card by {methods}? ').lower()
            return self.get_card(chosen_method)

    def choose_card(self):
        print(f'This is the list of {str(self.player)} playable cards by colour: {show_cards_list(self.same_colour)}')
        print(f'This is the list of {str(self.player)} playable cards by value: {show_cards_list(self.same_value)}')
        print(f'This is the list of {str(self.player)} playable cards by wildcard: {show_cards_list(self.wildcard)}')
        chosen = self.choice_for_card()
        while chosen is False:
            chosen = self.choice_for_card()
        return chosen

    def play_card(self, chosen_card, remove_from_hand):
        self.chosen_card = chosen_card
        if remove_from_hand:
            # Remove the card from hand list and playable
            self.player.hand.remove(chosen_card)
            self.player.playable_cards.remove(chosen_card)
        # Add the card to the discard pile
        self.deck.discard(chosen_card)
        print(f'{str(self.player)} plays the card {str(chosen_card)}')
        # TODO: self.shout_UNO_choice()

    def play(self, action):
        if self.player.bot or action is None:
            action = 'bot'

        reward = 0
        #  Decides to play a card
        if action == 'colour' or action == 'value' or action == 'wildcard':
            if (len(self.player.playable_cards) > 0):
                chosen_card = self.get_card(action)
                self.play_card(chosen_card, True)
                reward = int(chosen_card.score)
            else:
                reward = -1
        #  Decides to draw a card
        else:
            # If have a playable card in hand, penalise it
            if (len(self.player.playable_cards) > 0):
                    reward = -1
            else:
            # draw a card and receive the reward if can play with it; if not possible to play, no change in the reward.
                print(f'{str(self.player)} is drawing a card')
                card_drawn = self.deck.draw_card()
                if (self.player.is_playable(card_drawn, self.card_on_pile)):
                    self.play_card(card_drawn, False)
                    reward = int(card_drawn.score)
                else:
                    # add card to hand and next turn
                    self.player.hand.append(card_drawn)
                    print(f'{str(self.player)} pass the turn')

        self.evaluate_hand()
        if self.game_over:
            reward = reward + 1000

        return self.turn_message(), reward, self.game_over
        