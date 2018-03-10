import prev1
import new1
import exc3


def run_for_profiling(n, m, p, q, streams):
    for f in [prev1.proper_dividers_list, prev1.proper_dividers_fun, prev1.proper_dividers_map, new1.proper_dividers_iter]:
        f(n)

    for f in [prev1.primes_list, prev1.primes_fun, prev1.primes_map, new1.primes_iter]:
        f(m)

    for f in [prev1.perfect_numbers_list, prev1.perfect_numbers_fun, new1.perfect_numbers_iter]:
        f(p)

    while q > 0:
        for stream in streams:
            sentences = list(iter(exc3.Sentences(stream)))

            for sentence in sentences:
                exc3.Sentences.correct(sentence)

        q -= 1


n = 1000
m = 1000
p = 1000
q = 1000000
streams = open('The Hunger Games.txt')

run_for_profiling(n, m, p, q, streams)

streams.close()

# python -m profile 9.2.py

# 4: python "C:\Users\Maksymilian Zawartko\AppData\Local\Programs\Python\Python36-32\Lib\pydoc.py" -w <module name>