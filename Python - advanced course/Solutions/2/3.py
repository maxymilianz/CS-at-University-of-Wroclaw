import timeit

class ResException(BaseException):
    def __init__(self, n):
        self.n = n

def factorial_rec(n):
    return 1 if n == 0 else n * factorial_rec(n - 1)

def factorial_e(n):
    def factorial(n, acc):
        if n > 1:
            factorial(n - 1, acc * n)
        else:
            raise ResException(acc)

    try:
        factorial(n, 1)
    except ResException as e:
        return e.n

def fib_rec(n):
    return n if n < 2 else fib_rec(n - 1) + fib_rec(n - 2)

def fib_e(n):       # Idk what's the point in this excercise as exceptions are handled just as often as returns would
    def fib(n):
        if n < 2:
            raise ResException(n)
        else:
            try:
                fib(n - 1)
            except ResException as e:
                try:
                    fib(n - 2)
                except ResException as e1:
                    raise ResException(e.n + e1.n)

    try:
        fib(n)
    except ResException as e:
        return e.n

factorial_n = 500
fib_n = 20

factorial_rec_str = 'factorial_rec(' + str(factorial_n) + ')'
factorial_e_str = 'factorial_e(' + str(factorial_n) + ')'
fib_rec_str = 'fib_rec(' + str(fib_n) + ')'
fib_e_str = 'fib_e(' + str(fib_n) + ')'

print(factorial_rec_str, timeit.timeit(factorial_rec_str, 'from __main__ import factorial_rec', number = 10000))
print(factorial_e_str, timeit.timeit(factorial_e_str, 'from __main__ import factorial_e', number = 10000))

print(fib_rec_str, timeit.timeit(fib_rec_str, 'from __main__ import fib_rec', number = 10))
print(fib_e_str, timeit.timeit(fib_e_str, 'from __main__ import fib_e', number = 10))