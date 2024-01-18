from cards import deck_maker, shuffle_deck, deal_cards

number_players = int(input("Enter the number of players: "))
players = {}

for x in range(1, number_players+1):
    players['player-' + str(x)] = []

deck = deck_maker()
shuffle_deck(deck)
deal_cards(deck, players)

print(players)