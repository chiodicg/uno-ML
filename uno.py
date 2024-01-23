from cards import Card, Deck
from players import Player
from turn import Turn

number_players = int(input("Enter the number of players: "))
players = {}
turn_count = 0


for x in range(1, number_players+1):
    players['Player-' + str(x)] = Player('Player-' + str(x))
list_of_players = list(players.keys())

deck = Deck()
deck.deal_cards(players)

# Show each players' hand
for player in list_of_players:
    print(str(players[player]), players[player].show_hand())


deck.flip_card()
card_on_pile = deck.get_last_discarded()
print('discarded card', str(card_on_pile))


# For now, player 1 always start
# TODO: add number of games to play, and rotate who starts between the number of players

Turn(players['Player-1'], deck, card_on_pile)



