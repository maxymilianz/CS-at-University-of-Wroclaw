def quality(division):
    return sum(n * n for n in [len(word) for word in division])


def split_text(t, words):
    max_len = max(len(word) for word in words)

    def aux(t):
        if not t:
            return [], 0

        best_init = None
        best_tail_division = None
        best_q = 0

        init_len = 1        # first word length

        while init_len <= min(len(t), max_len):
            init = t[:init_len]

            if init in words:
                init_q = init_len * init_len
                tail_division, tail_q = aux(t[init_len:])

                if init_q + tail_q > best_q and tail_division != None:
                    best_init = init
                    best_tail_division = tail_division
                    best_q = init_q + tail_q

            init_len += 1

        if best_init and best_tail_division != None:
            return [best_init] + best_tail_division, best_q
        else:
            return None, 0

    return aux(t)[0]


def no_end_spaces(word):
    while word[-1].isspace():
        word = word[:-1]

    return word


def read_words(filename):
    with open(filename, encoding = 'utf8') as file:
        return set(no_end_spaces(w) for w in file)


def test_list():
    words = read_words('polish_words.txt')
    return split_text('tamatematykapustkinieznosi', words)


def test_mr_teddy():
    words = read_words('words_for_ai1.txt')
    with open('pan_tadeusz_bez_spacji.txt', encoding = 'utf8') as mr_teddy:
        for line in mr_teddy:
            print(' '.join(split_text(no_end_spaces(line), words)))