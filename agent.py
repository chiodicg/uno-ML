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
        self.model = Linear_QNet(9, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    '''
    States:
    - Do I have a card mathing value? True(1) or False(0)
    - Do I have a card matching colour? True(1) or False(0)
    - Do I have a wildcard? True(1) or False(0)

    Possible states:
    01) 0 0 0 -> no playable cards, draw
    02) 1 0 0 -> play colour
    03) 0 1 0 -> play value
    04) 0 0 1 -> play wildcard
    06) 1 1 0 -> play card (colour or value)
    07) 1 0 1 -> play card (colour or wild)
    08) 0 1 1 -> play card (wild or value)
    09) 1 1 1 -> play card (colour or value or wild)
    '''
    def get_state(self, game):
        state = [
            (len(game.match_colour) > 0),
            (len(game.match_value) > 0),
            (len(game.wildcard) > 0),
            game.game_over,
        ]
        np_state = np.array(state, dtype=int)
        print(state, np_state)

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


    def get_action(self, state):
        actions = ["colour", "value", "wildcard", 'draw']
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            choice = random.randint(0, 3)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            # Will predict a model with 4 values (output)
            prediction = self.model(state0)
            # Get which index is the max value -> use the same index to choose an action
            choice = torch.argmax(prediction).item()
            print(state0, prediction, torch.argmax(prediction), choice)

        print(choice, actions[choice])
        return actions[choice]


def train():
    # plot_win = []
    # plot_mean_win = []
    # total_turn = 0
    # turn_record = 1000
    agent = Agent()
    game = UNO_Game(2,1)
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get action (choose a card)
        choose_card = agent.get_action(state_old)

        # perform action and get the reward for this action or if the game is over
        # TODO: implement the play step on the game!
        reward, game_over = game.start_game(choose_card)
        print(reward, game_over, state_old, choose_card)

        # calculate the new state
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, choose_card, reward, state_new, game_over)

        agent.remember(state_old, choose_card, reward, state_new, game_over)

        if game_over:
            turn_count = game.turn_count
            # Reset game, increase the count, and train long memory, plot result
            game.reset()
            agent.number_games += 1
            agent.train_long_memory()

            # if turn_count < turn_record:
            #     # plot_win.append(game.winning_player)
            agent.model.save()

            print('Game', agent.number_games, 'Turns', turn_count)

            # total_score += score
            # mean_score = total_score / agent.n_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)



if __name__ == '__main__':
    train()