import random
from cards import Card, colours

def get_next_player(current_player, turn, number_players, play_direction):
    if turn == 0:
        next_player = 0
    else:
        if play_direction == 1:
            next_player = current_player + 1
            if next_player >= number_players:
                next_player = 0
        elif play_direction == -1:
            next_player = current_player - 1
            if next_player < 0:
                next_player = number_players - 1

    return next_player

def draw_cards(deck, number_of_cards, player):
    cards_drawn = deck.cards[:number_of_cards]
    del deck.cards[:number_of_cards]
    player.add_to_hand(cards_drawn)


def reverse_order(play_direction):
    if play_direction == 1:
        play_direction = -1
    else:
        play_direction = 1

def colour_chosen_validation(chosen_colour):
    if chosen_colour == '' or chosen_colour == 'random':
        return Card(random.choice(colours),None)
    elif not chosen_colour in colours:
        return False
    else:
        return Card(chosen_colour,None)
    
def colour_choice(player):
    if player.bot:
        return colour_chosen_validation('random')
    else:
        next_colour = str(input('Please, select a colour for the next round. The choices are: random, red, blue, green or yellow.')).lower()
        return colour_chosen_validation(next_colour)

def choose_colour(deck, player):
    next_colour = colour_choice(player)
    
    while next_colour is False:
        next_colour = colour_choice()
    
    deck.discard(next_colour)

def evaluate_card_played(deck):
    last_card = deck.get_last_discarded()
    # Evaluate if the card on the table is an action or wildcard, assing its value to the action for next turn (plus2, plus4, skip, reverse, colour)
    if isinstance(last_card.value, str):
        return last_card.value