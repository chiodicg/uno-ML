import os
from csv import writer, reader
from pathlib import Path
from shutil import rmtree
import numpy as np
import ast
from datetime import datetime

def write_data(path, data):
    with open(path, 'a') as csv_obj:
        writer_obj = writer(csv_obj)
        writer_obj.writerow(data)

        csv_obj.close()

def store_move(old_state, action, reward, new_state, game_over):
    rows = [old_state, action, reward, new_state, game_over]

    Path("train_data").mkdir(parents=True, exist_ok=True)

    current_timestamp = datetime.today().strftime('%d-%m-%Y_%H%M')
    file_name = 'training_' + current_timestamp + '.csv'
    write_data(f'train_data/{file_name}', rows)


def store_score(game_number, winner, number_of_turns):
    rows = [game_number, winner, number_of_turns]
    Path("train_data").mkdir(parents=True, exist_ok=True)

    current_timestamp = datetime.today().strftime('%d-%m-%Y_%H%M')
    file_name = 'scores_' + current_timestamp + '.csv'
    write_data(f'train_data/{file_name}', rows)