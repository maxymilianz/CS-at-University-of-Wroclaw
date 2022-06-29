letter_to_neighbours = {'q': 'wa',
                        'w': 'qase',
                        'e': 'ęwsdr',
                        'ę': 'ewsdr',
                        'r': 'edft',
                        't': 'rfgy',
                        'y': 'tghu',
                        'u': 'yhji',
                        'i': 'ujko',
                        'o': 'óiklp',
                        'ó': 'oiklp',
                        'p': 'ol',

                        'a': 'ąqwsz',
                        'ą': 'aqwsz',
                        's': 'śazxdew',
                        'ś': 'sazxdew',
                        'd': 'sxcfre',
                        'f': 'dcvgtr',
                        'g': 'fvbhyt',
                        'h': 'gbnjuy',
                        'j': 'hnmkiu',
                        'k': 'jmloi',
                        'l': 'łpok',
                        'ł': 'lpok',

                        'z': 'źżasx',
                        'ź': 'zżasx',
                        'ż': 'zźasx',
                        'x': 'źżzsdc',
                        'c': 'ćxdfv',
                        'ć': 'cxdfv',
                        'v': 'cfgb',
                        'b': 'vghn',
                        'n': 'ńbhjm',
                        'ń': 'nbhjm',
                        'm': 'njk'}


def deletion_cost(_: str) -> float:
    return 1


def insertion_cost(_: str) -> float:
    return 1


def substitution_cost(character_0: str, character_1: str) -> float:
    if character_1 in letter_to_neighbours and character_0 in letter_to_neighbours[character_1]:
        return .5
    else:
        return 1.5


def edit_distance(source: str, target: str) -> float:
    distances = [[0 for _ in range(len(target) + 1)]
                 for _ in range(len(source) + 1)]

    for i in range(len(source)):  # distances[0][0] == 0
        distances[i + 1][0] = distances[i][0] + deletion_cost(source[i])

    for j in range(len(target)):
        distances[0][j + 1] = distances[0][j] + insertion_cost(target[j])

    for i in range(len(source)):
        for j in range(len(target)):
            if source[i] == target[j]:
                distances[i + 1][j + 1] = distances[i][j]
            else:
                distances[i + 1][j + 1] = min(distances[i][j + 1] + deletion_cost(source[i]),
                                              distances[i + 1][j] + insertion_cost(target[j]),
                                              distances[i][j] + substitution_cost(source[i], target[j]))

    return distances[len(source)][len(target)]
