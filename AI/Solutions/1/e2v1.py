def split_text(t, words):
    t_len = len(t)
    max_len = 29        # MAGIC NUMBER, WORKS FOR 'words_for_ai1.txt'
    best_q = [(0, [])] * (t_len + 1)

    for i in range(1, t_len + 1):
        best_q[i] = max([(best_q[j][0] + len(t[j:i]) ** 2, best_q[j][1] + [t[j:i]]) for j in range(max(0, i - max_len), i) if t[j:i] in words] + [(0, [])],
                        key = lambda pair: pair[0])

    return best_q[-1][1]


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