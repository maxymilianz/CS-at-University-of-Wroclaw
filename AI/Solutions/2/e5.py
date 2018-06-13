from heapq import heappop, heappush
from queue import PriorityQueue
from random import choice
from sys import stdin


fields = wall, goal, start, start_goal, empty = '#GSB '
directions = up, down, left, right = 'UDLR'
neg_dir = {up: down, down: up, left: right, right: left, None: None}
dir_to_displacement = {up: (-1, 0), down: (1, 0), left: (0, -1), right: (0, 1)}


def print_maze(maze):
    for row in maze:
        print(''.join(row))


def extract_possibilities(maze):
    possibilities = set()

    for y in range(len(maze)):
        row = maze[y]

        for x in range(len(row)):
            if row[x] == start:
                possibilities |= {(y, x)}
                row[x] = empty
            elif row[x] == start_goal:
                possibilities |= {(y, x)}
                row[x] = goal

    return tuple(tuple(row) for row in maze), tuple(possibilities)


def move(maze, possibilities, direction):
    dy, dx = dir_to_displacement[direction]
    return tuple({(y + dy, x + dx) if maze[y + dy][x + dx] != wall else (y, x) for y, x in possibilities})


def solved(maze, possibilities):
    return all(maze[y][x] in {goal, start_goal} for y, x in possibilities)


def get_goals(maze):
    return {(y, x) for y in range(len(maze)) for x in range(len(maze[0])) if maze[y][x] == goal}


def solve(maze, possibilities, heuristic):
    # queue = PriorityQueue()
    q = []
    goals = get_goals(maze)
    # queue.put_nowait((heuristic(goals, possibilities), 0, possibilities, ''))
    heappush(q, (heuristic(goals, possibilities), 0, possibilities, ''))
    checked = {possibilities}

    while True:
        # _, cost, current_possibilities, path = queue.get_nowait()       # first, discarded, element of the tuple is estimated distance to a solution + cost
        _, cost, current_possibilities, path = heappop(q)

        for direction in directions:
            new_possibilities = move(maze, current_possibilities, direction)

            if new_possibilities not in checked:
                checked |= {new_possibilities}
                new_path = path + direction

                if not solved(maze, new_possibilities):
                    new_cost = cost + 1
                    # queue.put_nowait((new_cost + heuristic(goals, new_possibilities), new_cost, new_possibilities, new_path))
                    heappush(q, (new_cost + heuristic(goals, new_possibilities), new_cost, new_possibilities, new_path))
                else:
                    return new_path


def manhattan_dist(pos0, pos1):
    y0, x0 = pos0
    y1, x1 = pos1
    return abs(y0 - y1) + abs(x0 - x1)


def best_goal_dist(goals, pos):
    return min(manhattan_dist(pos, goal) for goal in goals)


def best_dist_sum(goals, possibilities):     # NOT OPTIMISTIC AND NOT CONSISTENT HEURISTIC
    return sum(best_goal_dist(goals, pos) for pos in possibilities)


def max_best_dist(goals, possibilities):
    return max(best_goal_dist(goals, pos) for pos in possibilities)


def max_best_dist_mult_poss(goals, possibilities):       # NOT OPTIMISTIC AND NOT CONSISTENT HEURISTIC
    return max_best_dist(goals, possibilities) * len(possibilities)


def count_poss_not_on_goals(goals, possibilities):      # NOT OPTIMISTIC AND NOT CONSISTENT HEURISTIC
    return len(set(possibilities) - set(goals))


def read_from_data(data):
    return [[ch for ch in line if ch in fields] for line in data.readlines()]    


def read_input(filename):
    if filename:
        with open(filename) as data:
            return read_from_data(data)
    else:
        return read_from_data(stdin)


def solve_from_file(filename, heuristic):
    maze = read_input(filename)
    maze, possibilities = extract_possibilities(maze)
    path = solve(maze, possibilities, heuristic)
    return len(path), path


print(solve_from_file(None, max_best_dist)[1])        # e5, for validator with --stdio
# print(solve_from_file(None, max_best_dist_mult_poss)[1])        # e6