from collections import deque
from functools import reduce
from operator import or_
from random import choice, shuffle
from time import time


empty, black, white = ',', '#', '-'

opposite_color = {black: white, white: black}

directions = {(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1), (1, 0), (1, 1)}

corners = {(0, 0), (7, 0), (0, 7), (7, 7)}
buffers = {(0, 1), (1, 0), (1, 1),
           (7, 1), (6, 0), (6, 1),
           (0, 6), (1, 7), (1, 6),
           (7, 6), (6, 7), (6, 6)}
edges = {(y, 0) for y in range(2, 6)} | {(y, 7) for y in range(2, 6)} | {(0, x) for x in range(2, 6)} | {(7, x) for x in range(2, 6)}

fields_rating = [[99, -8, 8, 6, 6, 8, -8, 99],
                 [-8, -24, -4, -3, -3, -4, -24, -8],
                 [8, -4, 7, 4, 4, 7, -4, 8],
                 [6, -3, 4, 0, 0, 4, -3, 6],
                 [6, -3, 4, 0, 0, 4, -3, 6],
                 [8, -4, 7, 4, 4, 7, -4, 8],
                 [-8, -24, -4, -3, -3, -4, -24, -8],
                 [99, -8, 8, 6, 6, 8, -8, 99]]


def print_board(board):
    print('\n'.join(''.join(row) for row in board))


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
            result += [(new_board, {field for field in empty_fields if field not in bounded_fields})]

    return result


def moves_dict(board, empty_fields, color):
    result = {}

    for y, x in empty_fields:
        bounded_fields = reduce(or_, (bounded(board, color, y, x, *direction) for direction in directions))
        if bounded_fields:
            new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
            result.update({(y, x): (new_board, {field for field in empty_fields if field not in bounded_fields})})

    return result


def alpha_beta(board, empty_fields, color, best_black, best_white):
    if not empty_fields:
        if color == black:
            return board, empty_fields, len([(y, x) for y in range(8) for x in range(8) if board[y][x] == black])
        else:
            return board, empty_fields, len([(y, x) for y in range(8) for x in range(8) if board[y][x] == white])

    quality = 0
    best_move = None

    for new_board, new_empty_fields in moves(board, empty_fields, color):
        _, _, opposite_quality = alpha_beta(new_board, new_empty_fields, opposite_color[color], best_black, best_white)
        new_quality = 64 - opposite_quality

        if new_quality > quality:
            quality = new_quality
            best_move = new_board, new_empty_fields

            if color == black:
                best_black = max(best_black, quality)
                if quality <= best_white:
                    break
            else:
                best_white = max(best_white, quality)
                if quality <= best_black:
                    break

    if best_move:
        return best_move + (quality,)
    else:
        return board, empty_fields, quality


def alpha_beta_player(board, empty_fields, color):
    board, empty_fields, _ = alpha_beta(board, empty_fields, color, 0, 0)       # third, discarded item is move quality
    return board, empty_fields


def eager_random_player(board, empty_fields, color):
    possibilities = moves(board, empty_fields, color)
    if possibilities:
        return choice(possibilities)
    else:
        return board, empty_fields


def random_player(board, empty_fields, color):     # much faster than eager_random_player
    empty_fields_list = list(empty_fields)
    shuffle(empty_fields_list)

    for y, x in empty_fields_list:
        bounded_fields = all_bounded_fields(board, color, y, x)
        if bounded_fields:
            new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
            return new_board, {field for field in empty_fields if field not in bounded_fields}

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


class MonteCarloPlayer:
    def __init__(self, branching_factor):
        self.quality = {}       # (board, empty_fields, color) -> quality
        self.child_moves = {}       # (board, empty_fields, color) -> {(board, empty_fields)}
        self.branching_factor = branching_factor

    def monte_carlo(self, board, empty_fields, color):
        possibilities = moves(board, empty_fields, color)
        self.child_moves[(board, empty_fields, color)] = possibilities

        if not possibilities:
            self.child_moves[(board, empty_fields, color)] = {(board, empty_fields)}
            black_count, white_count = count_score(board)

            if black_count > white_count:
                self.quality[(board, empty_fields, color)] = 1
                self.quality[(board, empty_fields, opposite_color[color])] = 0
                return 1, 0
            elif black_count < white_count:
                self.quality[(board, empty_fields, color)] = 0
                self.quality[(board, empty_fields, opposite_color[color])] = 1
                return 0, 1
            else:
                self.quality[(board, empty_fields, color)] = 0
                self.quality[(board, empty_fields, opposite_color[color])] = 0
                return 0, 0

        black_wins, white_wins = 0, 0

        for new_board, new_empty_fields in possibilities[:self.branching_factor]:
            rec_black_wins, rec_white_wins = self.monte_carlo(new_board, new_empty_fields, opposite_color[color])
            black_wins += rec_black_wins
            white_wins += rec_white_wins

        self.quality[(board, empty_fields, color)] = black_wins if color == black else white_wins

        return black_wins, white_wins

    def __call__(self, board, empty_fields, color):
        if (board, empty_fields, color) not in self.child_moves:
            self.monte_carlo(board, empty_fields, color)

        best_move = max(self.child_moves[(board, empty_fields, color)], key = lambda move: self.quality.get(move, 0))

        if best_move:
            return best_move
        else:
            return board, empty_fields


class MonteCarloRandomPlayer:
    def __init__(self, simulations_count):
        self.simulations_count = simulations_count

    def play(self, board, empty_fields, color):
        not_moved = False

        while empty_fields:
            not_moved = False
            new_board, empty_fields = random_player(board, empty_fields, color)

            if not empty_fields:
                break

            if new_board == board:
                not_moved = True

            new_board, empty_fields = random_player(board, empty_fields, opposite_color[color])

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

    def __call__(self, board, empty_fields, color):
        possibilities = {move: [self.play(*move, color) for i in range(self.simulations_count)].count(color) for move in moves(board, empty_fields, color)}

        if possibilities:
            board, empty_fields = max(possibilities, key = lambda move: possibilities[move])

        return board, empty_fields


# noticeably worse than positional_parity_player, but not in direct confrontation
def corners_player(board, empty_fields, color):
    def aux():
        nonlocal board
        nonlocal empty_fields
        nonlocal  color

        possibilities = []

        for y, x in empty_fields:
            bounded_fields = reduce(or_, (bounded(board, color, y, x, *direction) for direction in directions))
            if bounded_fields:
                new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
                possibilities += [(new_board, bounded_fields)]

        if not possibilities:
            return board, empty_fields

        corners_possibilities = [(board, bounded_fields) for board, bounded_fields in possibilities if bounded_fields & corners & set(empty_fields)]
        if corners_possibilities:
            return corners_possibilities[0]

        non_buffer_possibilities = [(board, bounded_fields) for board, bounded_fields in possibilities if not bounded_fields & buffers & set(empty_fields)]
        if non_buffer_possibilities:
            return non_buffer_possibilities[0]

        return possibilities[0]

    best_board, best_bounded_fields = aux()
    return best_board, tuple(field for field in empty_fields if field not in best_bounded_fields)


def positional_player(board, empty_fields, color):
    rated_empty_fields = sorted(list(empty_fields), key = lambda pos: fields_rating[pos[0]][pos[1]], reverse = True)

    for y, x in rated_empty_fields:
        bounded_fields = reduce(or_, (bounded(board, color, y, x, *direction) for direction in directions))
        if bounded_fields:
            new_board = tuple(tuple(field if (y, x) not in bounded_fields else color for x, field in enumerate(row)) for y, row in enumerate(board))
            return new_board, {field for field in empty_fields if field not in bounded_fields}

    return board, empty_fields


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


# best yet
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


def is_stable(board, color, y, x):
    for dy, dx in directions:
        new_y, new_x = y + dy, x + dx

        while 0 <= new_y < 8 and 0 <= new_x < 8:
            if board[new_y][new_x] == empty:
                return False
            new_y += dy
            new_x += dx

    return True


def count_stable_fields(board, color):
    result = 0

    for y, row in enumerate(board):
        for x, field in enumerate(row):
            if field == color and is_stable(board, color, y, x):
                result += 1

    return result


def stable_player(board, empty_fields, color):
    possibilities = moves(board, empty_fields, color)

    if possibilities:
        return max(possibilities, key = lambda p: count_stable_fields(p[0], color))
    else:
        return board, empty_fields


def stable_parity_player(board, empty_fields, color):
    empty_field_to_move = moves_dict(board, empty_fields, color)

    if not empty_field_to_move:
        return board, empty_fields

    possibilities = sorted(list((empty_field, move) for empty_field, move in empty_field_to_move.items()), key = lambda p: count_stable_fields(p[1][0], color))

    for (y, x), move in possibilities:
        if region_size(board, y, x) % 2 != 0:
            return move

    return possibilities[0][1]


def positional_parity_stable_heuristic(board, empty_fields, color):
    return 15 * count_stable_fields(board, color) + sum(fields_rating[y][x] for y in range(8) for x in range(8) if board[y][x] == color)


class HeuristicPlayer:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def __call__(self, board, empty_fields, color):
        possibilities = moves(board, empty_fields, color)

        if possibilities:
            return max(possibilities, key = lambda p: self.heuristic(p[0], p[1], color))
        else:
            return board, empty_fields


def play(black_player, white_player):
    board = create_board()
    empty_fields = {(y, x) for y in range(8) for x in range(8) if board[y][x] == empty}
    not_moved = False

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
