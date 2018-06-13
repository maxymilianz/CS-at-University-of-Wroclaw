from ReversiAux import *

from pickle import dump, load
from random import randrange
from sklearn.neural_network import MLPClassifier, MLPRegressor
from time import time

max_turns_count = 60


def play_n_turns(board, n, color):
    turn = 0
    empty_fields = {(y, x) for y in range(8) for x in range(8) if board[y][x] == empty}

    while turn < n:
        board, empty_fields = random_player(board, empty_fields, color)

        if not empty_fields:
            break

        turn += 1
        color = opposite_color[color]

    return board


def custom_play(board, color):
    empty_fields = {(y, x) for y in range(8) for x in range(8) if board[y][x] == empty}

    while empty_fields:
        not_moved = False
        new_board, empty_fields = random_player(board, empty_fields, color)

        if not empty_fields:
            break

        if new_board == board:
            not_moved = True

        color = opposite_color[color]
        new_board, empty_fields = random_player(new_board, empty_fields, color)

        if not_moved and new_board == board:
            break

        color = opposite_color[color]
        board = new_board

    black_count, white_count = count_score(board)

    if black_count > white_count:
        return black
    elif black_count < white_count:
        return white
    else:
        return None


def generate_data(count, random_games_count):
    data = []

    for i in range(count):
        turns = randrange(max_turns_count)
        board = play_n_turns(create_board(), turns, black)

        color = black if turns % 2 == 0 else white
        result = {black: 0, white: 0, None: 0}
        for i in range(random_games_count):
            result[custom_play(board, color)] += 1

        data += [(board, result)]

    return data


def regressor(data):
    # nn = MLPRegressor(hidden_layer_sizes = (60, 60, 10))
    nn = MLPRegressor()
    nn.fit(*data)
    return nn


def custom_regressor(data_size, random_games_count):
    data = generate_data(data_size, random_games_count)
    data = [sum(sample[0], ()) for sample in data], [sample[1][black] / data_size for sample in data]
    return regressor(data)


def custom_regressor_to_file(data_size, random_games_count, filename):
    with open(filename, 'w') as file:
        dump(custom_regressor(data_size, random_games_count), file)


def neural_network_to_file(nn, filename):
    with open(filename, 'wb') as file:
        dump(nn, file)


def neural_network_from_file(filename):
    with open(filename, 'rb') as file:
        return load(file)


def custom_regressor_through_file(data_size, random_games_count, filename):
    nn = custom_regressor(data_size, random_games_count)
    neural_network_to_file(nn, filename)
    return nn


def custom_regressor_through_file_time(data_size, random_games_count, filename):
    a = time()

    nn = custom_regressor(data_size, random_games_count)
    neural_network_to_file(nn, filename)

    b = time()
    print(b - a)

    return nn


# for now, I assume this player always plays black
class RegressionPlayer:
    def __init__(self, nn):
        self.nn = nn

    def __call__(self, board, empty_fields, color):
        possibilities = moves(board, empty_fields, color)

        if possibilities:
            return max(possibilities, key = lambda p: (1 if color == black else -1) * self.nn.predict([sum(p[0], ())]))
        else:
            return board, empty_fields


class ClassificationPlayer:
    def __init__(self, nn):
        self.nn = nn

    def __call__(self, board, empty_fields, color):
        possibilities = moves(board, empty_fields, color)

        if possibilities:
            return max(possibilities, key = lambda p: self.nn.predict_proba([sum(p[0], ())])[0][1 if color == black else 0])
        else:
            return board, empty_fields


def classifier_fit_from_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        data = [line.split() for line in lines]
        results, boards = [int(case[0]) for case in data], [list(case[1]) for case in data]
        boards = [[empty if field == '_' else black if field == '1' else white for field in board] for board in boards]

    # nn = MLPClassifier(hidden_layer_sizes = (60, 60, 10))
    nn = MLPClassifier()
    nn.fit(boards, results)
    return nn


def bigger_classifier():
    return classifier_fit_from_file('reversi_learning_data/bigger.dat')


def smaller_classifier():
    return classifier_fit_from_file('reversi_learning_data/smaller.dat')


def bigger_classifier_through_file():
    nn = bigger_classifier()
    neural_network_to_file(nn, 'bigger_classifier.dat')
    return nn


def smaller_classifier_through_file():
    nn = smaller_classifier()
    neural_network_to_file(nn, 'smaller_classifier.dat')
    return nn


def custom_bigger_classifier_through_file(hidden_layer_sizes, filename):
    with open('reversi_learning_data/bigger.dat') as file:
        lines = file.readlines()
        data = [line.split() for line in lines]
        results, boards = [int(case[0]) for case in data], [list(case[1]) for case in data]
        boards = [[empty if field == '_' else black if field == '1' else white for field in board] for board in boards]

    nn = MLPClassifier(hidden_layer_sizes = hidden_layer_sizes)
    nn.fit(boards, results)
    neural_network_to_file(nn, filename)
    return nn
