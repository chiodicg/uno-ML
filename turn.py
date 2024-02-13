from cards import show_cards_list
from actions import draw_cards
import random
from actions import draw_cards, analyse_hand


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
    def __init__(self, player, deck, plus2_counter):
        self.player = player
        self.deck = deck
        self.card_on_pile = deck.get_last_discarded()
        self.game_over = False
        self.chosen_card = None
        print(f'The card on the table is {str(self.card_on_pile)}. It is {str(self.player)} turn.')
        self.find_playable()
        print(f'{str(self.player)} has {len(self.player.playable_cards)} playable cards', show_cards_list(self.player.playable_cards))
        self.same_colour = [card for card in self.player.playable_cards if card.colour == self.card_on_pile.colour]
        self.same_value = [card for card in self.player.playable_cards if card.value == self.card_on_pile.value]
        self.wildcard = [card for card in self.player.playable_cards if card.colour == "wild"]
        self.count_colours, self.predominant_colours = analyse_hand(player.hand)
        self.choices = {
            'colour': {'low': [card for card in self.same_colour if card.score <= 4], 'high': [card for card in self.same_colour if card.score > 4 and card.score < 10], 'action': [card for card in self.same_colour if card.score > 20], 'any': self.same_colour},
            'value': {'predominant': [card for card in self.same_value if any(card.colour.startswith(colour.lower()) for colour in self.predominant_colours)], 'any': self.same_value},
            'wildcard': {'any': self.wildcard}
        }
        self.reward = 0
        self.plus2_counter = plus2_counter
        
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
        if len(self.player.hand) == 1:
            # if self.player.bot:
            shout = random.choice([True, False])
            # else:
            #     shout = self.shout_UNO_choice()

            # if not shout:
            #     draw_cards(self.deck, 2, self.player)
            # else:
            print(f'{str(self.player)} shouts UNO!')
        elif len(self.player.hand) == 0:
            self.game_over = True
        print(f'{str(self.player)} has {len(self.player.hand)} in its hand')

    def find_playable(self):
        self.player.find_playable_card(self.card_on_pile)
        self.player.playable_cards.sort(key=lambda card: sort_by_number(card), reverse=True)

    def get_card(self, chosen_method, subselection):
        if chosen_method == 'colour' or chosen_method == 'value' or chosen_method == 'wildcard':
            if len(self.choices[chosen_method]['any']) == 0 or len(self.choices[chosen_method][subselection]) == 0:
                self.reward = self.reward - 50
                return self.player.playable_cards[0]
            else:
                return self.choices[chosen_method][subselection][0]
        elif chosen_method == 'bot':
            return self.player.playable_cards[0]
        else:
            return self.player.playable_cards[random.randint(0, len(self.player.playable_cards)-1)]

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

    def draw_card_to_play(self):

        # draw a card and receive the reward if can play with it; if not possible to play, no change in the reward.
            print(f'{str(self.player)} is drawing a card')
            card_drawn = self.deck.draw_card()
            if (self.player.is_playable(card_drawn, self.card_on_pile)):
                self.play_card(card_drawn, False)
                print(card_drawn)
                self.reward = self.reward + int(card_drawn.score)
            else:
                # add card to hand and next turn
                self.player.hand.append(card_drawn)
                print(f'{str(self.player)} pass the turn')

    def play(self, action):
        breakdown_action = action.split('-')
        action = breakdown_action[0]
        subaction = None
        if len(breakdown_action) > 1:
            subaction = breakdown_action[1]

        if (len(self.player.playable_cards) > 0):
                if (self.card_on_pile.value == 'plus2' and any(card.value == 'plus2' for card in self.player.playable_cards)):
                    if action == 'value':
                        self.reward = self.reward + 20
                        self.plus2_counter = self.plus2_counter + 2
                    else:
                        self.reward = self.reward - 20
                        self.plus2_counter = 2
                chosen_card = self.get_card(action, subaction)
                self.play_card(chosen_card, True)
                self.reward = self.reward + int(chosen_card.score)
        else:
            # draw a card and receive the reward if can play with it; if not possible to play, no change in the reward.
            print(f'{str(self.player)} is drawing a card')
            card_drawn = self.deck.draw_card()
            if (self.player.is_playable(card_drawn, self.card_on_pile)):
                self.play_card(card_drawn, False)
                self.reward = self.reward + int(card_drawn.score)
            else:
                # add card to hand and next turn
                self.player.hand.append(card_drawn)
                print(f'{str(self.player)} pass the turn')

        self.evaluate_hand()
        if self.game_over:
            self.reward = self.reward + 1000
        print(self.turn_message())
        return self.reward
        