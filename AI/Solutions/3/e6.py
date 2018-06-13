def variable(y, x):
    return 'V' + str(y) + '_' + str(x)


def generate_row(y, columns_count, row):
    return '+'.join(variable(y, x) for x in range(columns_count)) + ' #= ' + str(row)


def generate_rows(rows_count, columns_count, rows):
    return ''.join(generate_row(y, columns_count, rows[y]) + ',\n' for y in range(rows_count))


def generate_column(x, rows_count, column):
    return '+'.join(variable(y, x) for y in range(rows_count)) + ' #= ' + str(column)


def generate_columns(rows_count, columns_count, columns):
    return ''.join(generate_column(x, rows_count, columns[x]) + ',\n' for x in range(columns_count))


def generate_rectangles(rows_count, columns_count):
    return ''.join(variable(y, x) + ' + ' + variable(y + 1, x) + ' + ' + variable(y, x + 1) + ' + ' + variable(y + 1, x + 1) + ' #\\= 3,\n'
                   for y in range(rows_count - 1) for x in range(columns_count - 1))


def ensure_rectangles_size(rows_count, columns_count):
    return ''.join('(' + variable(y, x) + ' #= 1) #==> (' + variable(y + 1, x) + ' + ' + variable(y - 1, x) + ' #> 0),\n'
                   for y in range(1, rows_count - 1) for x in range(columns_count)) + \
           ''.join('(' + variable(y, x) + ' #= 1) #==> (' + variable(y, x + 1) + ' + ' + variable(y, x - 1) + ' #> 0),\n'
                   for y in range(rows_count) for x in range(1, columns_count - 1))


def generate_output(columns_count):
    heads = ', '.join('H' + str(x) for x in range(columns_count))
    return 'output([]) :- !.\noutput(X) :-\n[' + heads + '|T] = X, write([' + heads + ']), ' + "write('\\n'), output(T)."


def storms(rows, columns, declarations):
    rows_count, columns_count = len(rows), len(columns)

    variables = [variable(y, x) for y in range(rows_count) for x in range(columns_count)]
    constraints = [var + ' in 0..1' for var in variables]

    rows_clauses = generate_rows(rows_count, columns_count, rows)
    columns_clauses = generate_columns(rows_count, columns_count, columns)
    rectangles_clauses = generate_rectangles(rows_count, columns_count)
    rectangles_size_clauses = ensure_rectangles_size(rows_count, columns_count)

    return ':- use_module(library(clpfd)).\n' + 'solve([' + ', '.join(variables) + ']) :- ' + ''.join(c + ', ' for c in constraints) + \
           ''.join(variable(y, x) + ' #= ' + v for y, x, v in declarations) + ',\n' + rows_clauses + '\n' + columns_clauses + '\n' + rectangles_clauses + '\n' + \
           rectangles_size_clauses + '\n    labeling([ff], [' + ', '.join(variables) + ']).\n\n' + generate_output(columns_count) + '\n:- solve(X), output(X), nl.'


def storms_from_to(src, dst):
    with open(src) as data:
        rows = data.readline().split()
        columns = data.readline().split()
        declarations = [line.split() for line in data.readlines()]

        with open(dst, 'w') as file:
            file.write(storms(rows, columns, declarations))
