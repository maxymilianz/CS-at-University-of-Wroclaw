import sys


def V(i, j):
    return 'V%d_%d' % (i, j)


def domains(Vs):
    return [q + ' in 1..9' for q in Vs]


def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'


def get_column(j):
    return [V(i, j) for i in range(9)]


def get_raw(i):
    return [V(i, j) for j in range(9)]


def horizontal():
    return [all_different(get_raw(i)) for i in range(9)]


def vertical():
    return [all_different(get_column(j)) for j in range(9)]


def print_constraints(Cs, indent, d):
    position = indent
    print((indent - 1) * ' ', )
    for c in Cs:
        print(c + ',', )
        position += len(c)
        if position > d:
            position = indent
            print()
            print((indent - 1) * ' ', )


def get_square(y, x):
    return [V(i, j) for i in range(y, y + 3) for j in range(x, x + 3)]


def squares():
    return [all_different(get_square(y, x)) for y in [0, 3, 6] for x in [0, 3, 6]]


def sudoku(assignments):
    variables = [V(i, j) for i in range(9) for j in range(9)]

    print(':- use_module(library(clpfd)).')
    print('solve([' + ', '.join(variables) + ']) :- ')

    cs = domains(variables) + vertical() + horizontal() + squares()  # TODO: too weak constraints, add something!
    for i, j, val in assignments:
        cs.append('%s #= %d' % (V(i, j), val))

    print_constraints(cs, 4, 70),
    print()
    print('    labeling([ff], [' + ', '.join(variables) + ']).')
    print()
    print(':- solve(X), write(X), nl.')


def main():
    raw = 0
    triples = []

    for x in sys.stdin:
        x = x.strip()
        if len(x) == 9:
            for i in range(9):
                if x[i] != '.':
                    triples.append((raw, i, int(x[i])))
            raw += 1
    sudoku(triples)


def solve(data):
    raw = 0
    triples = []

    for x in data.readlines():
        x = x.strip()
        if len(x) == 9:
            for i in range(9):
                if x[i] != '.':
                    triples.append((raw, i, int(x[i])))
            raw += 1
    sudoku(triples)


def solve_from_file(filename):
    if filename:
        with open(filename) as data:
            solve(data)
    else:
        solve(sys.stdin)


"""
89.356.1.
3...1.49.
....2985.
9.7.6432.
.........
.6389.1.4
.3298....
.78.4....
.5.637.48

53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79

3.......1
4..386...
.....1.4.
6.924..3.
..3......
......719
........6
2.7...3..
.........
"""
