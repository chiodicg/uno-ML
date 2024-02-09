from csv import writer, reader
from pathlib import Path
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython import display
import matplotlib.animation as animation

current_timestamp = datetime.today().strftime('%d-%m-%Y')

def write_data(path, data):
    with open(path, 'a') as csv_obj:
        writer_obj = writer(csv_obj)
        writer_obj.writerow(data)

        csv_obj.close()

def store_move(old_state, action, reward, new_state, game_over):
    rows = [old_state, action, reward, new_state, game_over]

    Path("train_data").mkdir(parents=True, exist_ok=True)

    file_name = 'training_' + current_timestamp + '.csv'
    write_data(f'train_data/{file_name}', rows)


def store_score(game_number, winner, number_of_turns):
    rows = [game_number, winner, number_of_turns]
    Path("train_data").mkdir(parents=True, exist_ok=True)

    file_name = 'scores_' + current_timestamp + '.csv'
    write_data(f'train_data/{file_name}', rows)

plt.ion()

def plot(wins, players):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.ylabel('Number of Wins')
    plt.xlabel('Players')
    plt.bar(players, wins)
    plt.pause(.1)