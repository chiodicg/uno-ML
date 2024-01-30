from cards import Deck, show_cards_list
from players import Player
from turn import Turn
from actions import get_next_player,draw_cards,reverse_order, choose_colour, evaluate_card_played

class UNO_Game:
    def __init__(self, number_players=None, number_bots=None):
        self.number_players = number_players
        self.number_bots = number_bots
        self.players = {}
        self.get_players()
        self.turn_count = 0
        self.game_over = False
        self.play_direction = 1
        self.current_player = 0
        self.action_preturn = 'plus2'
        self.plus2_counter = 2
        self.list_of_players = list(self.players.values())
        self.winning_player = None
        self.deck = Deck()

    def get_players(self):
        if self.number_players is None:
            self.number_players = int(input("Enter the number of players: "))
        if self.number_bots is None:
            self.number_bots = int(input("Enter the number of players that are bots (random selection of cards): "))
        for player_number in range(1, self.number_players+1):
            self.players['Player-' + str(player_number)] = Player('Player-' + str(player_number), player_number <= self.number_bots)

    def __str__(self):
        return f'End of the game, with {self.turn_count} turns. {self.winning_player} wins.'

    def initialise_game(self):
        self.deck.deal_cards(self.players)
        self.deck.flip_card()

    def start_game(self):
        self.initialise_game()
        # For now, player 1 always start
        # TODO: add number of games to play, and rotate who starts between the number of players
        while not self.game_over:
            if self.action_preturn:
                current = self.list_of_players[self.current_player]
                next_player = self.list_of_players[get_next_player(self.current_player, self.turn_count, self.number_players, self.play_direction)]
                if self.action_preturn == 'plus2':
                    if not any(card.value == 'plus2' for card in next_player.hand):
                        print(f'{str(next_player)} draws {self.plus2_counter} cards')
                        draw_cards(self.deck, self.plus2_counter, next_player)
                        self.plus2_counter = 2
                    else:
                        self.plus2_counter = self.plus2_counter + 2
                if self.action_preturn == 'plus4':
                    print(f'Player hand: {show_cards_list(current.hand)}')
                    choose_colour(self.deck, current)
                    print(f'{str(next_player)} draws 4 cards')
                    draw_cards(self.deck, 4, next_player)
                elif self.action_preturn == 'colour':
                    print(f'Player hand: {show_cards_list(current.hand)}')
                    choose_colour(self.deck, current)
                elif self.action_preturn == 'reverse':
                    reverse_order(self.play_direction)
                elif self.action_preturn == 'skip':
                    #  Get next player. This will then be skipped, because the same code will run again before the turn.
                    self.current_player = get_next_player(self.current_player, self.turn_count, self.number_players, self.play_direction)
                self.action_preturn = None

            self.current_player = get_next_player(self.current_player, self.turn_count, self.number_players, self.play_direction)
            turn = str(Turn(self.list_of_players[self.current_player], self.deck))
            if turn.startswith('Game over'):
                self.winning_player = str(self.list_of_players[self.current_player])
                self.game_over = True
                print(turn)
            else:
                self.action_preturn = evaluate_card_played(self.deck)
                self.turn_count += 1

        return f'End of the game, with {self.turn_count} turns. {self.winning_player} wins.'

print(UNO_Game(2,2).start_game())
UNO_Game().start_game()




