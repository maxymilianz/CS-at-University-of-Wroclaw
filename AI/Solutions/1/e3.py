from random import shuffle
from itertools import product
from functools import reduce
from operator import or_


suit = ['d', 'c', 'h', 's']
blots = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
figures = ['j', 'q', 'k', 'a']

power = {'high': 0, 'pair': 1, 'two_pairs': 2, 'three': 3, 'straight': 4, 'flush': 5, 'full': 6, 'quads': 7, 'poker': 8}


def best_set(hand):
    def pair():
        no_colors = [c[0] for c in hand]
        return reduce(or_, [[card for card in no_colors].count(c) == 2 for c in no_colors])

    def two_pairs():
        no_colors = [c[0] for c in hand]
        return len([c for c in set(no_colors) if no_colors.count(c) == 2]) == 2

    def three():
        no_colors = [c[0] for c in hand]
        return reduce(or_, [[card for card in no_colors].count(c) == 3 for c in no_colors])

    def straight():
        no_colors = [c[0] for c in hand]
        no_colors_set = set(no_colors)
        blots_count = len(blots)
        for i in range(blots_count - len(hand)):
            if no_colors_set == set(blots[i:i+5]):
                return True
        return False

    def flush():
        return len(set([c[1] for c in hand])) == 1

    def full():
        return pair() and three()

    def quads():
        no_colors = [c[0] for c in hand]
        return reduce(or_, [[card for card in no_colors].count(c) == 4 for c in no_colors])

    def poker():
        return straight() and flush()

    if poker():
        return 'poker'
    elif quads():
        return 'quads'
    elif full():
        return 'full'
    elif flush():
        return 'flush'
    elif straight():
        return 'straight'
    elif three():
        return 'three'
    elif two_pairs():
        return 'two_pairs'
    elif pair():
        return 'pair'
    else:
        return 'high'


def random_blots(n):
    options = list(product(blots, suit))
    shuffle(options)
    return options[:n]


def random_pair_blots(n):
    options = list(product(blots, suit))
    shuffle(options)
    return [options[0]] + options[:n-1]


def random_two_pairs_blots(n):
    options = list(product(blots, suit))
    shuffle(options)
    return [options[0], options[1]] + options[:n-2]


def random_three_blots(n):
    options = list(product(blots, suit))
    shuffle(options)
    return [options[0]] * 2 + options[:n-2]


def random_straight_blots(n):
    return list(product(blots, suit))[:n]       # no matter what straight it is, so don't waste time randomizing


def random_flush_blots(n):
    options = list(product(blots, [suit[0]]))       # no matter what color it is, so don't waste time randomizing
    shuffle(options)
    return options[:n]


def random_full_blots(n):
    options = list(product(blots, suit))
    shuffle(options)
    return [options[0]] * 2 + [options[1]] * 3


def random_quads_blots(n):
    options = list(product(blots, suit))
    shuffle(options)
    return [options[0]] * 3 + options[:n-3]


def random_poker_blots(n):
    options = list(product(blots, [suit[0]]))       # no matter what poker it is, so don't waste time randomizing
    return options[:n]


def random_figures(n):
    options = list(product(figures, suit))
    shuffle(options)
    return options[:n]


def compare(hand0, hand1):      # works only for simplified case of this excercise and not for real poker
    set0, set1 = best_set(hand0), best_set(hand1)
    return power[set0] > power[set1]


def test_best_set():
    blots, figures = random_blots(5), random_figures(5)
    print(blots, best_set(blots))
    print(figures, best_set(figures))


def test_extended(test_count, blots_generator):
    blotter_wins = 0

    for i in range(test_count):
        blots, figures = blots_generator(5), random_figures(5)

        if compare(blots, figures):
            blotter_wins += 1

    return blotter_wins / test_count


def test(test_count):
    return test_extended(test_count, random_blots)


# test(1000000) = 0.082204

# following results are bad

# test_extended(10000, random_pair_blots) = 0.3047
# test_extended(10000, random_two_pairs_blots) = 0.5326
# test_extended(10000, random_three_blots) = 0.8097
# test_extended(10000, random_straight_blots) = 0.988
# test_extended(10000, random_flush_blots) = 0.9219
# test_extended(10000, random_full_blots) = 0.8326
# test_extended(10000, random_quads_blots) = 0.8904
# test_extended(10000, random_poker_blots) = 1