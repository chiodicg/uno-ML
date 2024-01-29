from cards import Deck
from players import Player
from turn import Turn
from actions import get_next_player,draw_cards,reverse_order, choose_colour, evaluate_card_played

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

# # Show each players' hand
# for player in list_of_players:
#     print(str(player), player.show_hand())

deck.flip_card()

# For now, player 1 always start
# TODO: add number of games to play, and rotate who starts between the number of players

while not game_over:
    if action_preturn:
        if action_preturn == 'plus4' or action_preturn == 'plus2':
            player = list_of_players[get_next_player(current_player, turn_count, number_players, play_direction)]
            draw_cards(deck, int(action_preturn[-1]), player)
            if action_preturn == 'plus4':
                choose_colour(deck)
        elif action_preturn == 'colour':
            choose_colour(deck)
        elif action_preturn == 'reverse':
            reverse_order(play_direction)
        elif action_preturn == 'skip':
            #  Get next player. This will then be skipped, because the same code will run again before the turn.
            current_player = get_next_player(current_player, turn_count, number_players, play_direction)
        action_preturn = None

    current_player = get_next_player(current_player, turn_count, number_players, play_direction)
    card_on_pile = deck.get_last_discarded()
    turn = str(Turn(list_of_players[current_player], deck, card_on_pile))
    if turn.startswith('Game over'):
        game_over = True
        print(turn)
    else:
        action_preturn = evaluate_card_played(deck)
        turn_count += 1

print('turns:', turn_count)



