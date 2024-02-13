import torch
import random
import numpy as np
from collections import deque
from uno import UNO_Game
from model import Linear_QNet, QTrainer
from data import store_move, store_score, plot, get_filename, rename_last_dataset

MAX_MEMORY = 100_000
BATCH_SIZE=1_000
LR = 0.001

class Agent:
    def __init__(self, number_of_games=1000):
        self.game_count = 0
        self.epsilon = 0 # rate of random actions (exploration)
        self.gamma = 0.9 # discount rate -> closer to 1 gives more importance to reward at the end
        self.memory = deque(maxlen=MAX_MEMORY) # queue for memory; when full, it will automatically remove the element on the left
        self.model = Linear_QNet(7, 256, 6)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.game = None
        self.number_of_games = number_of_games
        self.game_over = False
        self.number_wins = 0
        self.number_loses = 0

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    """  Possible states and actions:
        0) Play matching colour low number (<= 4)
        1) Play matching colour high number (> 4)
        2) Play matching colour action
        3) Play matching number of predominant colour
        4) Play matching number any colour
        5) Play wildcard
        6) Draw
    """
    def get_action(self, state):
        
        action = [0,0,0,0,0,0]
        choice = None
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.game_count
        if random.randint(0, 200) < self.epsilon:
            choice = random.randint(0, 5)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            # Will predict a model with 3 values (output)
            prediction = self.model(state0)
            # Get which index is the max value -> use the same index to choose an action
            choice = torch.argmax(prediction).item()
        
        action[choice] = 1
        return action
    
    def handle_end_of_turn(self, game_over):
        if game_over:
            turn_count = self.game.turn_count
            winning_player = self.game.winning_player
            self.train_long_memory()
            model_name = get_filename('model', '.pth')
            self.model.save(model_name)
            print(f'Game: {self.game_count}, Turns: {str(turn_count)}, Winner: {winning_player}')
            store_score(self.game_count, winning_player, turn_count)
            if winning_player == 'Player-2':
                self.number_wins += 1
            else:
                self.number_loses += 1
            last_game = self.game_count == self.number_of_games
            plot([self.number_loses, self.number_wins], ['Player-1: PC', 'Player-2: AI'], last_game)
    
    def handle_turn(self):
        game = self.game
        current_state = game.get_state()
        action = self.get_action(current_state)
        list_actions = {0: 'colour-low', 1: 'colour-high', 2: 'colour-action', 3: 'value-predominant', 4: 'value-any', 5: 'wildcard-any', 6: 'draw'}
        translated_action = list_actions[action.index(max(action))]

        reward = game.turn.play(translated_action)

        # calculate the new state
        new_state = game.get_state()
        self.game_over = game.turn.game_over

        # train short memory
        self.train_short_memory(current_state, action, reward, new_state, self.game_over)

        self.remember(current_state, action, reward, new_state, self.game_over)

        store_move(current_state, action, reward, new_state, self.game_over)
    
    def start(self):
        for _ in range(0,self.number_of_games):
            self.reset_game()


    def reset_game(self):
        self.game = UNO_Game(2,1,self.handle_end_of_turn)
        self.game.play_notifier('Player-2', self.handle_turn)
        self.game_count += 1
        print('Starting new game...')
        self.game_over = False
        self.game.start_game()


if __name__ == '__main__':
    agent = Agent(1)
    agent.start()
    print('Number of wins: ' + str(agent.number_wins))
    print('Number of losses: ' + str(agent.number_loses))
    rename_last_dataset()