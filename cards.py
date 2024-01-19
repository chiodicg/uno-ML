import random

colours = ["red", "green", "blue", "yellow"]
wildcards = ["wild-colour", "wild-plus4"]

def deck_maker():
    deck = wildcards*4
    for colour in colours:
        for value in range(0,10):
            deck.append(colour + "-" + str(value))
            if (value != 0):
                deck.append(colour + "-" + str(value))
        for wild in ["reverse", "plus2", "skip"]*2:
            deck.append(colour + "-" + wild)
    return deck

def shuffle_deck(deck):
    return random.shuffle(deck)

def flip_card(deck, pile):
    pile.append(deck.pop())

def deal_cards(deck, players, pile):
    for x in range(0,7):
        for player in list(players.keys()):
            players[player].append(deck.pop())
    
    # Flip first card
    while len(pile)<1 or pile[-1].startswith('wild'):
        flip_card(deck, pile)
    
