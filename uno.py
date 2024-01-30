from cards import Deck, show_cards_list
from players import Player
from turn import Turn
from actions import get_next_player,draw_cards,reverse_order, choose_colour, evaluate_card_played

number_players = int(input("Enter the number of players: "))
number_bots = int(input("Enter the number of players that are bots (random selection of cards): "))
players = {}
turn_count = 0
game_over = False
play_direction = 1
current_player = 0
action_preturn = 'plus2'
plus2_counter = 2

for player_number in range(1, number_players+1):
    players['Player-' + str(player_number)] = Player('Player-' + str(player_number), player_number <= number_bots)
list_of_players = list(players.values())

deck = Deck()
deck.deal_cards(players)

# # Show each players' hand
# for player in list_of_players:
#     print(str(player), player.show_hand(), str(player.bot))

deck.flip_card()

# For now, player 1 always start
# TODO: add number of games to play, and rotate who starts between the number of players

while not game_over:
    if action_preturn:
        current = list_of_players[current_player]
        next_player = list_of_players[get_next_player(current_player, turn_count, number_players, play_direction)]
        if action_preturn == 'plus2':
            if not any(card.value == 'plus2' for card in next_player.hand):
                print(f'{str(next_player)} draws {plus2_counter} cards')
                draw_cards(deck, plus2_counter, next_player)
                plus2_counter = 2
            else:
                plus2_counter = plus2_counter + 2
        if action_preturn == 'plus4':
            print(f'Player hand: {show_cards_list(current.hand)}')
            choose_colour(deck, current)
            print(f'{str(next_player)} draws 4 cards')
            draw_cards(deck, 4, next_player)
        elif action_preturn == 'colour':
            print(f'Player hand: {show_cards_list(current.hand)}')
            choose_colour(deck, current)
        elif action_preturn == 'reverse':
            reverse_order(play_direction)
        elif action_preturn == 'skip':
            #  Get next player. This will then be skipped, because the same code will run again before the turn.
            current_player = get_next_player(current_player, turn_count, number_players, play_direction)
        action_preturn = None

    current_player = get_next_player(current_player, turn_count, number_players, play_direction)
    turn = str(Turn(list_of_players[current_player], deck))
    if turn.startswith('Game over'):
        game_over = True
        print(turn)
    else:
        action_preturn = evaluate_card_played(deck)
        turn_count += 1

print('turns:', turn_count)



