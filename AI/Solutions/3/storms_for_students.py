def B(i, j):
    return 'B_%d_%d' % (i, j)


def storms(raws, cols, triples):
    writeln(':- use_module(library(clpfd)).')

    R = len(raws)
    C = len(cols)

    bs = [B(i, j) for i in range(R) for j in range(C)]

    writeln('solve([' + ', '.join(bs) + ']) :- ')

    # TODO: add some constraints

    writeln('    [%s] = [1,1,0,1,1,0,1,1,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],' % (', '.join(bs),))  # only for test 1

    writeln('    labeling([ff], [' + ', '.join(bs) + ']).')
    writeln('')
    writeln(":- solve(X), write(X), nl.")


def writeln(s):
    output.write(s + '\n')


txt = open('tests/6.1.in').readlines()
output = open('storms_for_students.pl', 'w')

raws = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(map(int, txt[i].split()))

storms(raws, cols, triples)
