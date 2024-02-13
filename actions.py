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

def get_colour_chosen(chosen_colour):
    if chosen_colour in colours:
        return Card(chosen_colour,None)
    else:
        return Card(random.choice(colours), None, 0)
    
def colour_choice():
    next_colour = str(input('Please, select a colour for the next round. The choices are: random, red, blue, green or yellow.')).lower()
    return get_colour_chosen(next_colour)

def choose_colour(deck, player, choice):
    if player.bot:
        choice = 'random'
    next_colour = get_colour_chosen(choice)
    deck.discard(next_colour)
    

def evaluate_card_played(deck):
    last_card = deck.get_last_discarded()
    # Evaluate if the card on the table is an action or wildcard, assing its value to the action for next turn (plus2, plus4, skip, reverse, colour)
    if isinstance(last_card.value, str):
        return last_card.value
    
def count_colours(hand):
    count = {'R': 0, 'G': 0, 'Y': 0, 'B': 0, 'W': 0}
    count['R'] = len([card for card in hand if card.colour == 'red'])
    count['G'] = len([card for card in hand if card.colour == 'green'])
    count['Y'] = len([card for card in hand if card.colour == 'yellow'])
    count['B'] = len([card for card in hand if card.colour == 'blue'])
    count['W'] = len([card for card in hand if card.colour == 'wild'])

    return count

def predominant(count):
    return [keys for keys,values in count.items() if values == max(count.values())]

def analyse_hand(hand):
    count = count_colours(hand)
    return count, predominant(count)
