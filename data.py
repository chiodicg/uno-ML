from csv import writer, reader
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from IPython import display
import os
import collections

wins = collections.Counter()
def analyse_scores_file(file):
    total_games = 0
    with open(file) as input_file:
        for row in reader(input_file, delimiter=','):
            wins[row[1]] += 1
            total_games += 1
    
    print('AI wins: %s' % wins['Player-2'])
    print(wins)
    print(f'Total Games: {total_games}' )
    print(f'% AI Wins: {round(wins["Player-2"]/total_games * 100, 1)}')
    print(f'% PC Wins: {round(wins["Player-1"]/total_games * 100, 1)}')

current_timestamp = datetime.today().strftime('%d-%m-%Y')

def write_data(path, data):
    with open(path, 'a') as csv_obj:
        writer_obj = writer(csv_obj)
        writer_obj.writerow(data)
        csv_obj.close()

def get_filename(initial, extension):
    path = './model/' if initial == 'model' else './train_data/'
    count = 0
    filename = initial + '_' + current_timestamp + '_' + str(count) + extension
    while os.path.exists(path + filename):
        count += 1
        filename = initial + '_' + current_timestamp + '_' + str(count) + extension
    return filename

def rename_last_dataset():
    path = './train_data/'
    renamed_scores = get_filename('scores', '.csv')
    renamed_training = get_filename('training', '.csv')
    renamed_model = get_filename('model', '.pth')
    os.rename(path + 'training_' + current_timestamp + '.csv', path + renamed_training)
    os.rename(path + 'scores_' + current_timestamp + '.csv', path + renamed_scores)
    os.rename('./model/' + 'model.pth', './model/' + renamed_model)

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

def plot(wins, players, last_game):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.ylabel('Number of Wins')
    plt.xlabel('Players')
    plt.bar(players, wins)
    plt.pause(.1)
    if last_game:
        plt.savefig('train_data/' + get_filename('training_plot','.png'))