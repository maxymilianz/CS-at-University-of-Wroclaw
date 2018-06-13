from itertools import permutations
from functools import lru_cache
from queue import PriorityQueue, Queue
from time import time


empty, wall, agent, crate, goal, crate_on_goal, agent_on_goal = '.WKBG*+'
directions = up, down, left, right = 'UDLR'


def print_board(board):
    for row in board:
        print(''.join(row), end = '')
    print()


class Counter:
    def __init__(self):
        self.i = 0

    def counter(self):
        self.i += 1
        return self.i


def trivial_heuristic(board):
    return 0


def count_crates_not_on_goals(board):
    return sum(row.count(crate) for row in board)


def manhattan_distance(pos0, pos1):
    return abs(pos0[0] - pos1[0]) + abs(pos0[1] - pos1[1])


def crates(board):
    h, w = len(board), len(board[-1])       # I'm checking width in last row, because it may be shorter as it may not contain '\n'
    crates = set()
    
    for y in range(h):
        for x in range(w):
            if board[y][x] in {crate, crate_on_goal}:
                crates |= {(y, x)}

    return crates


def goals(board):
    h, w = len(board), len(board[-1])
    goals = set()
    
    for y in range(h):
        for x in range(w):
            if board[y][x] in {goal, crate_on_goal, agent_on_goal}:
                goals |= {(y, x)}

    return goals


def best_manhattan_distance(board):
    return min(sum(manhattan_distance(crate, goal) for crate, goal in zip(crates_perm, goals_perm))
               for crates_perm in permutations(crates(board)) for goals_perm in permutations(goals(board)))


@lru_cache(maxsize = None)
def greedy_manhattan_distance(board):
    crates_list, goals_list = list(crates(board)), list(goals(board))
    distance = 0

    for crate in crates_list:
        distances = [manhattan_distance(crate, goal) for goal in goals_list]
        best_distance = min(distances)
        distance += best_distance
        del goals_list[distances.index(best_distance)]

    return distance


def solved(board):
    return not any(crate in row for row in board)


def neighbour(pos, direction):
    y, x = pos

    if direction == up:
        return y - 1, x
    elif direction == down:
        return y + 1, x
    elif direction == left:
        return y, x - 1
    elif direction == right:
        return y, x + 1


@lru_cache(maxsize = None)
def on_board(pos, board):
    y, x = pos
    return y in range(len(board)) and x in range(len(board[-1]))


def agent_move(board, agent_pos, direction):
    pos = y, x = neighbour(agent_pos, direction)
    
    if on_board(pos, board) and board[y][x] in {empty, goal}:
        return pos
    else:
        return None


def agent_moves(board, agent_pos):
    agent_moves = set()

    for direction in directions:
        pos = agent_move(board, agent_pos, direction)
        if pos:
            agent_moves |= {(pos, direction)}

    return agent_moves


def achievable_fields(board, agent_pos):
    queue = Queue()
    queue.put_nowait((agent_pos, ''))
    pos_to_path = {agent_pos: ''}

    while not queue.empty():
        agent_pos, path = queue.get_nowait()

        for new_agent_pos, direction in agent_moves(board, agent_pos):
            if new_agent_pos not in pos_to_path:
                new_path = path + direction
                pos_to_path[new_agent_pos] = new_path
                queue.put_nowait((new_agent_pos, new_path))

    return pos_to_path


@lru_cache(maxsize = None)
def board_after_crate_move(board, crate_pos, new_crate_pos):
    return tuple(tuple(board[y][x] if (y, x) not in {crate_pos, new_crate_pos} else ((empty if board[y][x] == crate else goal) if (y, x) == crate_pos
                       else (crate if board[y][x] in {empty, agent} else crate_on_goal)) for x in range(len(board[y]))) for y in range(len(board)))


def crate_moves(crate, board, agent_pos, achievable_fields):
    crate_moves = []

    for direction, neg_direction in {(up, down), (down, up), (left, right), (right, left)}:
        new_agent_pos = neighbour(crate, neg_direction)

        if new_agent_pos in achievable_fields:
            new_crate = y, x = neighbour(crate, direction)

            if on_board(new_crate, board) and board[y][x] in {empty, agent, goal, agent_on_goal}:
                crate_moves += [(board_after_crate_move(board, crate, new_crate), crate, achievable_fields[new_agent_pos] + direction)]

    return crate_moves


def moves(board, agent_pos):
    fields = achievable_fields(board, agent_pos)
    return sum((crate_moves(crate, board, agent_pos, fields) for crate in crates(board)), [])


def solve(board, agent_pos, heuristic):
    queue = PriorityQueue()
    counter = Counter().counter
    queue.put_nowait((heuristic(board), counter(), board, agent_pos, ''))
    used_settings = set()

    while True:
        _, _, board, agent_pos, path = queue.get_nowait()

        if solved(board):
            return path

        for new_board, new_agent_pos, new_path in moves(board, agent_pos):
            if (new_board, new_agent_pos) not in used_settings:
                used_settings |= {(new_board, new_agent_pos)}
                queue.put_nowait((heuristic(new_board), counter(), new_board, new_agent_pos, path + new_path))


def read_file(filename):
    with open(filename) as data:
        lines = [list(line) for line in data.readlines()]

        for i in range(len(lines)):
            line = lines[i]
            if agent in line:
                y = i
                x = line.index(agent)
                line[x] = empty
                break
            elif agent_on_goal in line:
                y = i
                x = line.index(agent_on_goal)
                line[x] = goal
                break

        board = tuple(tuple(ch for ch in line) for line in lines)
        return board, (y, x)


def solve_from_file(filename, heuristic):
    board, agent_pos = read_file(filename)
    return solve(board, agent_pos, heuristic)


def test(filename, heuristics):
    board, agent_pos = read_file(filename)
    times = {}

    for heuristic in heuristics:
        a = time(); solve(board, agent_pos, heuristic); heuristic_time = time() - a
        times[heuristic.__name__] = heuristic_time

    return times


def test_many(filenames, heuristics):
    for filename in filenames:
        print(filename)
        for heuristic_name, time in test(filename, heuristics).items():
            print(heuristic_name + '\t' + str(time))
        print()


def test_default():
    test_many(['2.' + str(i) + '.in' for i in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]],
              [trivial_heuristic, count_crates_not_on_goals, best_manhattan_distance, greedy_manhattan_distance])


def test_default3():
    test_many(['3.' + str(i) + '.in' for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
              [count_crates_not_on_goals])


case_to_heuristic = {1: count_crates_not_on_goals,
                     2: count_crates_not_on_goals,
                     3: greedy_manhattan_distance,
                     4: greedy_manhattan_distance,
                     5: greedy_manhattan_distance,
                     6: count_crates_not_on_goals,
                     7: greedy_manhattan_distance,
                     8: count_crates_not_on_goals,
                     9: count_crates_not_on_goals,
                     10: count_crates_not_on_goals}


def test_best_heuristics():
    for case, heuristic in case_to_heuristic.items():
        filename = '3.' + str(case) + '.in'
        
        print(filename)
        for heuristic_name, time in test(filename, [heuristic]).items():
            print(heuristic_name + '\t' + str(time))
        print()

        greedy_manhattan_distance.cache_clear()
        on_board.cache_clear()
        board_after_crate_move.cache_clear()