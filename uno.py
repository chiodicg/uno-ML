from cards import Card, Deck
from players import Player

number_players = int(input("Enter the number of players: "))
players = {}


for x in range(1, number_players+1):
    players['Player-' + str(x)] = Player('Player-' + str(x))

deck = Deck()
deck.deal_cards(players)
deck.flip_card()
card_on_pile = deck.get_last_discarded()
print(str(card_on_pile))


# For now, player 1 always start
# TODO: add number of games to play, and rotate who starts between the number of players

"""
Each turn:
Players will play the cards in turns, one card at a time. Card must match colour, number or symbol
You may pickup a new card from the deck if you don't want to play or can't
If the card you pickup is the only playable card which you have then you can play it
"""
players['Player-1'].find_playable_card(card_on_pile)
print('Player 1 playable cards:', players['Player-1'].show_playable_cards())
# If player has a playable card, then choose one
if (len(players['Player-1'].playable_cards) > 0):
    pass
# Or draw a card
else:
    # draw card
    # evaluate card if playable
    # if not, pass;
    # if yes, play;
    pass

# Show each players' hand
for player in list(players.keys()):
    print(str(players[player]), players[player].show_hand())
# Show discard pile
print('discard pile', deck.show_discard_pile())