def rozklad(n):
    divider = 2
    dict = {}

    while n > 1:
        exp = 0

        while n % divider == 0:
            n /= divider
            exp += 1

        if exp != 0:
            dict[divider] = exp

        divider += 1

    return list(dict.items())