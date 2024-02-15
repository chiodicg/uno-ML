from cards import Deck, show_cards_list
from players import Player
from turn import Turn
from actions import get_next_player,draw_cards,reverse_order, choose_colour, evaluate_card_played, analyse_hand
import numpy as np
from statistics import mean

class UNO_Game:
    def __init__(self, number_players=None, number_bots=None, handle_end_of_turn=None):
        self.number_players = number_players
        self.number_bots = number_bots
        self.list_of_players =  self.get_players()
        self.handle_play = {}
        self.turn_count = 0
        self.game_over = False
        self.play_direction = 1
        self.current_player = 0
        self.action_preturn = 'plus2'
        self.plus2_counter = 2
        self.winning_player = None
        self.deck = Deck()
        self.reward = 0
        self.turn = None
        self.handle_end_of_turn = handle_end_of_turn

    def get_players(self):
        list_players = []
        if self.number_players is None:
            self.number_players = int(input("Enter the number of players: "))
        if self.number_bots is None:
            self.number_bots = int(input("Enter the number of players that are bots (random selection of cards): "))
        for player_number in range(1, self.number_players+1):
            list_players.append(Player('Player-' + str(player_number), player_number <= self.number_bots))
        return list_players

    def __str__(self):
        return f'End of the game, with {self.turn_count} turns. {self.winning_player} wins.'

    def initialise_game(self):
        self.deck.deal_cards(self.list_of_players)
        self.deck.flip_card()

    def get_state(self):
        last_card = self.deck.get_last_discarded()
        player = self.list_of_players[-1]
        opponent = self.list_of_players[0]
        player.find_playable_card(last_card)
        colour_counts, predominant_colours = analyse_hand(player.hand)
        matching_colour_numbered = [card for card in player.playable_cards if card.colour == last_card.colour and card.score <= 9]
        if len(matching_colour_numbered) > 0:
            average_score_matching_colours = mean([card.score for card in matching_colour_numbered])
        else:
            average_score_matching_colours = 0
        matching_numbers = [card for card in player.playable_cards if card.value == last_card.value]
        matching_colour_actions = [card for card in player.playable_cards if card.colour == last_card.colour and card.score >= 25]
        wildcards = [card for card in player.playable_cards if card.colour == 'wildcard']
        """ 
        1) How many matching colours numbered cards? Int
        2) Are coloured numbers average > 4? T/F
        3) How many matching colour actions? Int
        4) How many matching numbers? Int
        5) Any matching numbers in predominant colour? T/F
        6) How many wildcards? Int
        7) Does the opponent has less than 3 cards? T/F
        """
        state = [
        len(matching_colour_numbered),
        average_score_matching_colours > 4,
        len(matching_colour_actions),
        len(matching_numbers),
        len([card for card in matching_numbers if any(card.colour.startswith(colour.lower()) for colour in predominant_colours)]) > 0,
        len(wildcards),
        len(opponent.hand) < 3
        ]
        np_state = np.array(state, dtype=int)

        return np_state

    def check_preturn_action(self):
        if self.action_preturn:
            current = self.list_of_players[self.current_player]
            next_player = self.list_of_players[get_next_player(self.current_player, self.turn_count, self.number_players, self.play_direction)]
            if self.action_preturn == 'plus2':
                if not any(card.value == 'plus2' for card in next_player.hand):
                    print(f'{str(next_player)} draws {self.plus2_counter} cards')
                    draw_cards(self.deck, self.plus2_counter, next_player)
                    self.plus2_counter = 2
            if self.action_preturn == 'plus4':
                print(f'Player hand: {show_cards_list(current.hand)}')
                choose_colour(self.deck, current, 'random')
                print(f'{str(next_player)} draws 4 cards')
                draw_cards(self.deck, 4, next_player)
            elif self.action_preturn == 'colour':
                print(f'Player hand: {show_cards_list(current.hand)}')
                choose_colour(self.deck, current, 'random')
            elif self.action_preturn == 'reverse':
                reverse_order(self.play_direction)
            elif self.action_preturn == 'skip':
                #  Get next player. This will then be skipped, because the same code will run again before the turn.
                self.current_player = get_next_player(self.current_player, self.turn_count, self.number_players, self.play_direction)
            self.action_preturn = None

    def start_game(self):
        self.initialise_game()
        # For now, player 1 always start
        # TODO: add number of games to play, and rotate who starts between the number of players
        while not self.game_over:
        
            self.check_preturn_action()

            self.current_player = get_next_player(self.current_player, self.turn_count, self.number_players, self.play_direction)
            player = self.list_of_players[self.current_player]
            self.turn = Turn(player, self.deck, self.plus2_counter)

            if str(player) in self.handle_play:
                handler = self.handle_play.get(str(player))
                handler()
            else: 
                self.turn.play('bot')

            if self.turn.game_over:
                self.game_over = True
                self.winning_player = str(player)
            else:
                self.action_preturn = evaluate_card_played(self.deck)
                self.turn_count += 1

            if self.handle_end_of_turn != None:
                self.handle_end_of_turn(self.game_over)
            
    def play_notifier(self, player, handler):
        self.handle_play[player] = handler

# print(UNO_Game(2,2).start_game())
# UNO_Game().start_game()




