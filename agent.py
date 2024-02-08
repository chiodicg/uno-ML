import torch
import random
import numpy as np
from collections import deque
from uno import UNO_Game
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE=1_000
LR = 0.001

class Agent:
    def __init__(self):
        self.number_games = 0
        self.epsilon = 0 # rate of random actions (exploration)
        self.gamma = 0.9 # discount rate -> closer to 1 gives more importance to reward at the end
        self.memory = deque(maxlen=MAX_MEMORY) # queue for memory; when full, it will automatically remove the element on the left
        self.model = Linear_QNet(3, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.game = None

    '''
    States:
    - Do I have a card mathing value? True(1) or False(0)
    - Do I have a card matching colour? True(1) or False(0)
    - Do I have a wildcard? True(1) or False(0)
    '''
    def get_state(self, game):
        state = [
            (len(game.match_colour) > 0),
            (len(game.match_value) > 0),
            (len(game.wildcard) > 0)
        ]
        np_state = np.array(state, dtype=int)

        return np_state

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
        01) 0 0 0 -> no playable cards, draw
        02) 1 0 0 -> play colour
        03) 0 1 0 -> play value
        04) 0 0 1 -> play wildcard
        05) 1 1 0 -> play card (colour or value)
        06) 1 0 1 -> play card (colour or wild)
        07) 0 1 1 -> play card (wild or value)
        08) 1 1 1 -> play card (colour or value or wild) """
    def get_action(self, state):
        action = [0,0,0]
        choice = None
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.number_games
        if random.randint(0, 200) < self.epsilon:
            choice = random.randint(0, 2)
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
            self.number_games += 1
            winning_player = self.game.winning_player
            self.train_long_memory()
            self.model.save()
            print(f'Game: {self.number_games}, Turns: {str(turn_count)}, Winner: player {winning_player}')

            self.reset_game()
    
    def handle_turn(self):
        game = self.game
        current_state = self.get_state(game)
        action = self.get_action(current_state)

        reward = game.turn.play(action)

        # calculate the new state
        new_state = self.get_state(game)
        game_over = game.game_over

        # train short memory
        self.train_short_memory(current_state, action, reward, new_state, game_over)

        self.remember(current_state, action, reward, new_state, game_over)

    def get_game(self):
        if self.game == None:
            self.reset_game()
        return self.game
    
    def start(self):
        game = self.get_game()
        game.start_game()

    def reset_game(self):
        game = UNO_Game(2,1,self.handle_end_of_turn)
        self.game = game
        game.play_notifier('Player-2', self.handle_turn)
        game.start_game()


if __name__ == '__main__':
   agent = Agent()
   agent.start()