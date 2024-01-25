from cards import Card, Deck, colours
from players import Player
from turn import Turn
import random

number_players = int(input("Enter the number of players: "))
players = {}
turn_count = 0
game_over = False
play_direction = 1
current_player = 0
action_preturn = None


for x in range(1, number_players+1):
    players['Player-' + str(x)] = Player('Player-' + str(x))
list_of_players = list(players.values())

deck = Deck()
deck.deal_cards(players)

# Show each players' hand
for player in list_of_players:
    print(str(player), player.show_hand())

deck.flip_card()

def get_next_player(current_player, turn):
    global play_direction
    if turn == 0:
        next_player = 0
    else:
        if play_direction == 1:
            next_player = current_player + 1
            if next_player >= number_players:
                next_player = 0
        elif play_direction == -1:
            next_player = current_player - 1
            if next_player <= 0:
                next_player = number_players - 1

    return next_player

def draw_cards(number_of_cards, player):
    cards_drawn = deck.cards[:number_of_cards]
    del deck.cards[:number_of_cards]
    player.add_to_hand(cards_drawn)


def skip_player():
    global current_player
    #  Get next player. This will then be skipped, because the same code will run again before the turn.
    current_player = get_next_player(current_player, turn_count)

def reverse_order():
    global play_direction
    if play_direction == 1:
        play_direction = -1
        return
    else:
        play_direction = 1

def choose_colour():
    next_colour = Card(random.choice(colours),None)
    deck.discard(next_colour)

def evaluate_card_played():
    last_card = deck.get_last_discarded()
    # Evaluate if the card on the table is an action or wildcard, assing its value to the action for next turn (plus2, plus4, skip, reverse, colour)
    if isinstance(last_card.value, str):
        return last_card.value

# For now, player 1 always start
# TODO: add number of games to play, and rotate who starts between the number of players

while not game_over:
    for i in range(0, number_players):
        if game_over:
            pass
        else:
            if action_preturn:
                if action_preturn == 'plus4' or action_preturn == 'plus2':
                    player = list_of_players[get_next_player(current_player, turn_count)]
                    draw_cards(int(action_preturn[-1]), player)
                elif action_preturn == 'colour':
                    choose_colour()
                elif action_preturn == 'reverse':
                    reverse_order()
                elif action_preturn == 'skip':
                    skip_player()
                action_preturn = None

            current_player = get_next_player(current_player, turn_count)
            card_on_pile = deck.get_last_discarded()
            turn = str(Turn(list_of_players[current_player], deck, card_on_pile))
            if turn == 'True':
                game_over = True
            else:
                action_preturn = evaluate_card_played()
                turn_count += 1

print('turns:', turn_count)



