from random import randrange, choice
from functools import reduce
from operator import and_
from math import inf


def transpose(img):
    w, h = len(img), len(img[0])
    return [[img[x][y] for x in range(w)] for y in range(h)]


# def opt_dist_0(l, d):
#     return min([len(list(filter(lambda x: x == 1, l[:i]+l[i+d:])) + list(filter(lambda x: x == 0, l[i:i+d]))) for i in range(len(l) - d + 1)])


# def opt_dist_1(l, d):
#     return min([len(list(filter(lambda x: x == 1, l[:i]+l[i+d:]))) + len(list(filter(lambda x: x == 0, l[i:i+d]))) for i in range(len(l) - d + 1)])


def opt_dist(l, d):     # fastest
    return min([l[:i].count(1) + l[i+d:].count(1) + l[i:i+d].count(0) for i in range(len(l) - d + 1)])


# def random_seq01(n):
#     return [choice([False, True]) for i in range(n)]


# def test_opt_dist(n, i, v):
#     for j in range(i):
#         seq = random_seq01(n)
#         d = randrange(n)

#         if v == 0:
#             opt_dist_0(seq, d)
#         elif v == 1:
#             opt_dist_1(seq, d)
#         else:
#             opt_dist_2(seq, d)


def solved_column(column, pattern):
    return opt_dist(column, pattern) == 0


def solved_columns(img, columns):
    return reduce(and_, [solved_column(column, pattern) for column, pattern in zip(img, columns)])


def solved(img, columns, rows):
    return solved_columns(img, columns) and solved_columns(transpose(img), rows)


def choose_pixel(img, columns, rows):
    def best_y(img, x, columns, rows):
        diff, y = inf, None
        for i in range(len(img[x])):
            new_old_dist = opt_dist(img[x], columns[x]) + opt_dist(transpose(img)[i], rows[i])
            img[x][i] = not img[x][i]
            new_diff = opt_dist(img[x], columns[x]) + opt_dist(transpose(img)[i], rows[i]) - new_old_dist
            img[x][i] = not img[x][i]
            if new_diff < diff:
                diff, y = new_diff, i
        return y

    w, h = len(columns), len(rows)

    unsolved_cols = [x for x in range(w) if not solved_column(img[x], columns[x])]      # nrs of unsolved columns

    if unsolved_cols:
        x = choice(unsolved_cols)
        y = best_y(img, x, columns, rows)
        return x, y
    else:
        transposed = transpose(img)
        unsolved_rows = [y for y in range(h) if not solved_column(transposed[y], rows[y])]      # nrs of unsolved rows
        y = choice(unsolved_rows)
        x = best_y(transposed, y, rows, columns)
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


def solve(columns, rows, max_i = 1000):
    # columns and rows are lists of lists of ints
    # in img, first coord is x, second - y
    
    w, h = len(columns), len(rows)
    img = [[False for y in range(h)] for x in range(w)]
    success = solved(img, columns, rows)

    while not success:
        i = 0
        img = [[choice([False, True]) for y in range(h)] for x in range(w)]
        success = solved(img, columns, rows)

        while not success and i < max_i:
            x, y = choose_pixel(img, columns, rows)

            img[x][y] = not img[x][y]

            i += 1
            success = solved(img, columns, rows)

            # print_img(img)
            # print()

    return img


def test(max_i):
    cases = [([7,7,7,7,7,7,7], [7,7,7,7,7,7,7]), 
             ([2,2,7,7,2,2,2], [2,2,7,7,2,2,2]), 
             ([2,2,7,7,2,2,2], [4,4,2,2,2,5,5]),
             ([7,6,5,4,3,2,1], [1,2,3,4,5,6,7]),
             ([7,5,3,1,1,1,1], [1,2,3,7,3,2,1])]

    for columns, rows in cases:
        print_img(solve(columns, rows, max_i))
        print()