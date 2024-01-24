from cards import Card, Deck
from players import Player
from turn import Turn

number_players = int(input("Enter the number of players: "))
players = {}
turn_count = 0
game_over = False
play_direction = 1
current_player = 0


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
    if turn == 0:
        next_player = 0
    else:
        if play_direction == 1:
            next_player = current_player + 1
            if next_player > number_players:
                next_player = 0
        elif play_direction == -1:
            next_player = current_player - 1
            if next_player < 0:
                next_player = number_players

    return next_player

# For now, player 1 always start
# TODO: add number of games to play, and rotate who starts between the number of players

# while not game_over:
for i in range(0, number_players):
    current_player = get_next_player(current_player, turn_count)
    print(f'{str(list_of_players[current_player])} turn')
    card_on_pile = deck.get_last_discarded()
    print('discarded card', str(card_on_pile))
    Turn(list_of_players[current_player], deck, card_on_pile, game_over)
    turn_count += 1

print('turns:', turn_count)



