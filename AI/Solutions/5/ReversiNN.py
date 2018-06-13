from ReversiAux import *

from math import inf
from pickle import dump, load
from sklearn.neural_network import MLPClassifier


char_to_field = {'_': empty, '1': black, '0': white}

bigger_data = 'reversi_learning_data/bigger.dat'
smaller_data = 'reversi_learning_data/smaller.dat'


class ClassificationPlayer:
    def __init__(self, nn, tuned = False, custom = False):
        self.nn = nn
        self.tuned = tuned
        self.custom = custom

    def __call__(self, board, empty_fields, color):
        possibilities = moves(board, empty_fields, color)

        if possibilities:
            if self.tuned:
                if self.custom:
                    return max(possibilities,
                               key = lambda p: self.nn.predict_proba([custom_tune_board(list(sum(p[0], ())))])[0][1 if color == black else 0])
                else:
                    return max(possibilities,
                               key = lambda p: self.nn.predict_proba([tune_board(list(sum(p[0], ())))])[0][1 if color == black else 0])
            else:
                return max(possibilities, key = lambda p: self.nn.predict_proba([list(sum(p[0], ()))])[0][1 if color == black else 0])
        else:
            return board, empty_fields


def classifier(xs, ys, hidden_layer_sizes = (100,)):
    nn = MLPClassifier(hidden_layer_sizes)
    nn.fit(xs, ys)
    return nn


def data_from_file(filename):
    with open(filename) as file:
        results, boards = [], []

        for line in file:
            result, board = line.split()
            result = int(result)
            board = [char_to_field[char] for char in board]
            results += [result]
            boards += [board]

        return boards, results


def balance(board):
    black_count, white_count = board.count(black), board.count(white)
    return [black_count, white_count]


def corners_balance(board):
    black_corners = len([(y, x) for y, x in corners if board[y*8 + x] == black])
    white_corners = len([(y, x) for y, x in corners if board[y*8 + x] == white])
    return [black_corners, white_corners]


def buffers_balance(board):
    black_buffers = len([(y, x) for y, x in buffers if board[y*8 + x] == black])
    white_buffers = len([(y, x) for y, x in buffers if board[y*8 + x] == white])
    return [white_buffers, black_buffers]


def tune_board(board):
    return board + balance(board) + corners_balance(board) + buffers_balance(board)


def tune_data(boards, results):
    tuned_boards = [tune_board(board) for board in boards]
    return tuned_boards, results


def positional_balance(board):
    black_rating = sum(fields_rating[y][x] for y in range(8) for x in range(8) if board[y*8 + x] == black)
    white_rating = sum(fields_rating[y][x] for y in range(8) for x in range(8) if board[y*8 + x] == white)
    return [black_rating, white_rating]


def get_region(board, y, x):
    region = set()
    to_check = deque({(y, x)})

    while to_check:
        y, x = to_check.pop()

        if board[y*8 + x] == empty:
            region |= {(y*8 + x)}

            for new_y, new_x in {(y+1, x), (y-1, x), (y, x+1), (y, x-1)}:
                if 0 <= new_y < 8 and 0 <= new_x < 8 and (new_y*8 + new_x) not in region:
                    to_check.append((new_y, new_x))

    return region


def parity(board):
    empty_indexes = {i for i in range(64) if board[i] == empty}
    regions = []

    while empty_indexes:
        i = empty_indexes.pop()
        region = get_region(board, i // 8, i % 8)
        regions += [region]
        empty_indexes -= region

    return [len([region for region in regions if len(region) % 2 == 0])]


def custom_tune_board(board):
    return tune_board(board) + positional_balance(board) + parity(board)


def custom_tune_data(boards, results):
    tuned_boards = [custom_tune_board(board) for board in boards]
    return tuned_boards, results


def bigger_classification_player():
    return ClassificationPlayer(from_file('bigger_classifier.dat'))


def bigger_tuned_classification_player():
    return ClassificationPlayer(from_file('bigger_tuned_classifier.dat'), True)


def bigger_custom_tuned_classification_player():
    return ClassificationPlayer(from_file('bigger_custom_tuned_classifier.dat'), True, True)


def to_file(obj, filename):
    with open(filename, 'wb') as file:
        dump(obj, file)


def from_file(filename):
    with open(filename, 'rb') as file:
        return load(file)
