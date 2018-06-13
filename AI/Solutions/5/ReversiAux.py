from collections import deque
from functools import reduce
from operator import or_
from random import shuffle
from time import time


# empty, black, white = ',', '#', '-'
empty, black, white = 0, 1, 2

opposite_color = {black: white, white: black}

directions = {(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1), (1, 0), (1, 1)}

corners = {(0, 0), (7, 0), (0, 7), (7, 7)}
buffers = {(0, 1), (1, 0), (1, 1),
           (7, 1), (6, 0), (6, 1),
           (0, 6), (1, 7), (1, 6),
           (7, 6), (6, 7), (6, 6)}

fields_rating = [[99, -8, 8, 6, 6, 8, -8, 99],
                 [-8, -24, -4, -3, -3, -4, -24, -8],
                 [8, -4, 7, 4, 4, 7, -4, 8],
                 [6, -3, 4, 0, 0, 4, -3, 6],
                 [6, -3, 4, 0, 0, 4, -3, 6],
                 [8, -4, 7, 4, 4, 7, -4, 8],
                 [-8, -24, -4, -3, -3, -4, -24, -8],
                 [99, -8, 8, 6, 6, 8, -8, 99]]


def print_board(board):
    print('\n'.join(''.join(str(field) for field in row) for row in board))


def create_board():
    return ((empty,) * 8,) * 3 + ((empty,) * 3 + (white, black) + (empty,) * 3,) + ((empty,) * 3 + (black, white) + (empty,) * 3,) + ((empty,) * 8,) * 3


def bounded(board, color, y, x, dy, dx):     # color of player bounding
    result = {(y, x)}
    y += dy
    x += dx

    while 0 <= y < 8 and 0 <= x < 8 and board[y][x] not in {empty, color}:
        result |= {(y, x)}
        y += dy
        x += dx

    if not (0 <= y < 8 and 0 <= x < 8) or board[y][x] == empty or len(result) == 1:
        return set()
    else:
        return result


def all_bounded_fields(board, color, y, x):
    return reduce(or_, (bounded(board, color, y, x, *direction) for direction in directions))


def moves(board, empty_fields, color):
    result = []

    for y, x in empty_fields:
        bounded_fields = reduce(or_, (bounded(board, color, y, x, *direction) for direction in directions))
        if bounded_fields:
            new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
            result += [(new_board, tuple({field for field in empty_fields if field not in bounded_fields}))]

    return result


def moves_dict(board, empty_fields, color):
    result = {}

    for y, x in empty_fields:
        bounded_fields = reduce(or_, (bounded(board, color, y, x, *direction) for direction in directions))
        if bounded_fields:
            new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
            result.update({(y, x): (new_board, {field for field in empty_fields if field not in bounded_fields})})

    return result


def random_player(board, empty_fields, color):     # much faster than eager_random_player
    empty_fields_list = list(empty_fields)
    shuffle(empty_fields_list)

    for y, x in empty_fields_list:
        bounded_fields = all_bounded_fields(board, color, y, x)
        if bounded_fields:
            new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
            return new_board, tuple({field for field in empty_fields if field not in bounded_fields})

    return board, empty_fields


def count_score(board):
    black_count, white_count = 0, 0

    for row in board:
        for field in row:
            if field == black:
                black_count += 1
            elif field == white:
                white_count += 1

    return black_count, white_count


def region_size(board, y, x):
    region = set()
    to_check = deque({(y, x)})

    while to_check:
        y, x = to_check.pop()

        if board[y][x] == empty:
            region |= {(y, x)}

            for new_y, new_x in {(y+1, x), (y-1, x), (y, x+1), (y, x-1)}:
                if 0 <= new_y < 8 and 0 <= new_x < 8 and (new_y, new_x) not in region:
                    to_check.append((new_y, new_x))

    return len(region)


def positional_parity_player(board, empty_fields, color):
    rated_empty_fields = sorted(list(empty_fields), key = lambda pos: fields_rating[pos[0]][pos[1]], reverse = True)
    even_sized_regions = deque()

    for y, x in rated_empty_fields:
        if region_size(board, y, x) % 2 != 0:
            bounded_fields = all_bounded_fields(board, color, y, x)
            if bounded_fields:
                new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
                return new_board, {field for field in empty_fields if field not in bounded_fields}
        else:
            even_sized_regions.append((y, x))

    for y, x in even_sized_regions:
        bounded_fields = all_bounded_fields(board, color, y, x)
        if bounded_fields:
            new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
            return new_board, {field for field in empty_fields if field not in bounded_fields}

    return board, empty_fields


def play(black_player, white_player):
    board = create_board()
    empty_fields = tuple({(y, x) for y in range(8) for x in range(8) if board[y][x] == empty})

    while empty_fields:
        not_moved = False
        new_board, empty_fields = black_player(board, empty_fields, black)

        if not empty_fields:
            break

        if new_board == board:
            not_moved = True

        new_board, empty_fields = white_player(new_board, empty_fields, white)

        if not_moved and new_board == board:
            break

        board = new_board

    black_count, white_count = count_score(board)

    if black_count > white_count:
        return black
    elif black_count < white_count:
        return white
    else:
        return None


def test(black_player, white_player):
    result = play(black_player, white_player)
    if result == black:
        print('Black')
    elif result == white:
        print('White')
    else:
        print('Draw')


def test_n(n, black_player, white_player):
    result = {black: 0, white: 0, None: 0}
    for i in range(n):
        result[play(black_player, white_player)] += 1
    print('Black : White : Draw')
    print(result[black], ':', result[white], ':', result[None])


def test_n_time(n, black_player, white_player):
    a = time()
    test_n(n, black_player, white_player)
    b = time()
    print(b - a)
