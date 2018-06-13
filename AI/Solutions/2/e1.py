from collections import deque
from numpy import zeros
from sys import stdin


def print_img(img):
    for row in img:
        for cell in row:
            if cell:
                print('#', end = '')
            else:
                print('.', end = '')

        print()


def possibilities(n, pattern):
    def aux(n, pattern):
        if not n:
            return [[]]

        if not pattern:
            return [[0] * n]

        block_len = pattern[0]
        block = [1] * block_len
        new_n = n - block_len
        if pattern[1:]:
            block += [0]
            new_n -= 1
        current_possibilities = [block + new_pattern for new_pattern in aux(new_n, pattern[1:])]

        required_len = sum(pattern) + len(pattern) - 1
        if required_len < n:
            return current_possibilities + [[0] + new_pattern for new_pattern in aux(n - 1, pattern)]
        else:
            return current_possibilities

    return aux(n, pattern)


def solve(rows, columns):
    h, w = len(rows), len(columns)
    possible_rows = [possibilities(w, row) for row in rows]
    possible_columns = [possibilities(h, column) for column in columns]
    img = zeros((h, w))
    fixed = zeros((h, w))
    not_fixed = deque()

    def match_columns(y, x):
        b = img[y][x]
        possible_columns[x] = [column for column in possible_columns[x] if column[y] == b]

    def match_rows(y, x):
        b = img[y][x]
        possible_rows[y] = [row for row in possible_rows[y] if row[x] == b]

    def reason(y, x, current_rows):
        rb = current_rows[0][x]

        if all(row[x] == rb for row in current_rows):
            img[y][x] = rb
            fixed[y][x] = 1
            match_columns(y, x)
        else:
            cb = possible_columns[x][0][y]

            if all(column[y] == cb for column in possible_columns[x]):
                img[y][x] = cb
                fixed[y][x] = 1
                match_rows(y, x)
            else:
                not_fixed.append((y, x))

    for y in range(h):
        current_rows = possible_rows[y]
        for x in range(w):
            reason(y, x, current_rows)

    while not_fixed:
        y, x = not_fixed.popleft()
        current_rows = possible_rows[y]
        reason(y, x, current_rows)

    return img


def read_from_data(data):
    h, w = [int(literal) for literal in data.readline().split()]
    rows_and_columns = [[int(literal) for literal in line.split()] for line in data.readlines()]
    assert len(rows_and_columns) == h + w
    rows, columns = rows_and_columns[:h], rows_and_columns[h:]
    return rows, columns


def read_input(filename):
    if filename:
        with open(filename) as data:
            return read_from_data(data)
    else:
        return read_from_data(stdin)


def solve_from_file(filename):
    rows, columns = read_input(filename)
    print_img(solve(rows, columns))


def default_solve_from_file(case):
    rows, columns = read_input('tests/1.' + str(case) + '.in')
    print_img(solve(rows, columns))


solve_from_file(None)     # for validator