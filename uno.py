from cards import Card, Deck
from players import Player

number_players = int(input("Enter the number of players: "))
players = {}


for x in range(1, number_players+1):
    players['Player-' + str(x)] = Player('Player-' + str(x))

deck = Deck()
deck.deal_cards(players)
deck.flip_card()

for player in list(players.keys()):
    print(players[player].show_name(), players[player].show_hand())