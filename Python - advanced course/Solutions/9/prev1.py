from functools import reduce
from operator import add

def proper_dividers_list(n):
    """Function returning list of proper dividers of given number"""

    return [d for d in range(1, n) if n % d == 0]

def proper_dividers_fun(n):
    """Function returning list of proper dividers of given number"""

    return list(filter((lambda d: n % d == 0), range(1, n)))

def proper_dividers_map(n):
    """Function returning list of proper dividers of given number"""

    return list(map(proper_dividers_fun, range(n + 1)))

def primes_list(n):
    """Function returning list of primes less or equal given number"""

    return [p for p in range(n + 1) if proper_dividers_list(p) == [1]]

def primes_fun(n):
    """Function returning list of primes less or equal given number"""

    return list(filter((lambda n: proper_dividers_fun(n) == [1]), range(n + 1)))

def primes_map(n):
    """Function returning list of primes less or equal given number"""

    dividers = proper_dividers_map(n)
    return list(filter((lambda n: dividers[n] == [1]), range(n + 1)))

def perfect_numbers_list(n):
    """Function returning list of perfect numbers less or equal given number"""

    return [p for p in range(n + 1) if p == sum(proper_dividers_list(p))]

def perfect_numbers_fun(n):
    """Function returning list of perfect numbers less or equal given number"""

    return list(filter(lambda n: n == reduce(add, proper_dividers_fun(n), 0), range(n + 1)))