def proper_dividers_iter(n):
    """Function returning list of proper dividers of given number"""

    d = 1

    while d < n:
        if n % d == 0:
            yield d

        d += 1

class Primes:
    """Iterator class yielding primes"""

    def __init__(self):
        self.last = 1        # artificial, so that first call returns 2

    def __iter__(self):
        return self

    def __next__(self):
        n = self.last + 1

        while list(proper_dividers_iter(n)) != [1]:
            n += 1

        self.last = n
        return n

def primes_iter(n):
    """Function returning list of primes less or equal given number"""

    primes = iter(Primes())
    p = next(primes)

    while p <= n:
        yield p
        p = next(primes)

class PerfectNumbers:
    """Iterator class yielding perfect numbers"""

    def __init__(self):
        self.last = 1

    def __iter__(self):
        return self

    def __next__(self):
        n = self.last + 1

        while sum(proper_dividers_iter(n)) != n:
            n += 1

        self.last = n
        return n

def perfect_numbers_iter(n):
    """Function returning list of perfect numbers less or equal given number"""

    perfect_numbers = iter(PerfectNumbers())
    p = next(perfect_numbers)

    while p <= n:
        yield p
        p = next(perfect_numbers)