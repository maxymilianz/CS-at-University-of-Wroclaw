from random import randrange, choice
from functools import reduce
from operator import and_


def transpose(img):
    w, h = len(img), len(img[0])
    return [[img[x][y] for x in range(w)] for y in range(h)]


def solved_column(column, pattern):
    col_len = len(column)
    
    def next_1(i):
        while i < col_len and column[i] == 0:
            i += 1
        return i

    i = next_1(0)

    for n in pattern:
        group_match = len([b for b in column[i:i+n] if b]) == n
        if not group_match:
            return False
        i += n
        new_i = next_1(i)
        if i == new_i and i < col_len:
            return False
        i = new_i

    return i == col_len


def solved_columns(img, columns):
    return reduce(and_, [solved_column(column, pattern) for column, pattern in zip(img, columns)])


def solved(img, columns, rows):
    return solved_columns(img, columns) and solved_columns(transpose(img), rows)


def choose_pixel(img, columns, rows):
    def best_y(img, x):
        options = []
        for y in range(len(img[x])):
            img[x][y] = not img[x][y]
            options += [solved_column(img[x], columns[x]) + solved_column(transpose(img)[y], rows[y])]
            img[x][y] = not img[x][y]
        return options.index(max(options))

    w, h = len(columns), len(rows)

    unsolved_cols = [x for x in range(w) if not solved_column(img[x], columns[x])]      # nrs of unsolved columns

    if unsolved_cols:
        x = choice(unsolved_cols)
        y = best_y(img, x)
        return x, y
    else:
        transposed = transpose(img)
        unsolved_rows = [y for y in range(h) if not solved_column(transposed[y], rows[y])]      # nrs of unsolved rows
        y = choice(unsolved_rows)
        x = best_y(transposed, y)
        return x, y


def print_img(sol):
    transposed = transpose(sol)

    for row in transposed:
        for cell in row:
            if cell:
                print('#', end = '')
            else:
                print('.', end = '')

        print()


def solve(columns, rows, max_i):
    # columns and rows are lists of lists of ints
    # in img, first coord is x, second - y
    
    w, h = len(columns), len(rows)
    img = [[False for y in range(h)] for x in range(w)]
    success = solved(img, columns, rows)

    while not success:
        i = 0
        img = [[choice([False, True]) for y in range(h)] for x in range(w)]

        while not success and i < max_i:
            x, y = choose_pixel(img, columns, rows)

            img[x][y] = not img[x][y]

            i += 1
            success = solved(img, columns, rows)

    return img


def test(max_i = 1000):
    case0 = [[5],[1,1,1],[5],[1,1,1],[5]], [[5],[1,1,1],[5],[1,1,1],[5]]
    case1 = [[3],[1,1],[1,1,1],[1,1],[3]], [[3],[1,1],[1,1,1],[1,1],[3]]
    case2 = [[1,2],[4],[3],[4],[2,1]], [[2,1],[4],[3],[4],[1,2]]
    case3 = [[1,1,1],[1,1],[1,1,1],[1,1],[1,1,1]], [[1,1,1],[1,1],[1,1,1],[1,1],[1,1,1]]
    case4 = [[5],[1],[1],[1],[5]], [[1,1],[1,1],[5],[1,1],[1,1]]
    case5 = [[2,2], [2,2], [], [2,2], [2,2]], [[2,2], [2,2], [], [2,2], [2,2]]

    for columns, rows in [case0, case1, case2, case3, case4, case5]:
        print_img(solve(columns, rows, max_i))
        print()