from functools import reduce


substitutions = [
    ('ł', 'l'),  # Before ą, ę
    
    ('ą', 'a'),
    ('ol', 'a'),
    ('on', 'a'),
    ('om', 'a'),

    ('cia', 'ca'),
    ('cie', 'ce'),
    ('cio', 'co'),
    ('ciu', 'cu'),
    ('ć', 'c'),  # Before ch

    ('ę', 'e'),
    ('el', 'e'),
    ('en', 'e'),
    ('em', 'e'),

    ('ch', 'h'),

    ('nia', 'na'),
    ('nie', 'ne'),
    ('nio', 'no'),
    ('niu', 'nu'),
    ('ń', 'n'),

    ('o', 'u'),
    ('ó', 'u'),

    ('rz', 'z'),  # before z

    ('sia', 'sa'),
    ('sie', 'se'),
    ('sio', 'so'),
    ('siu', 'su'),
    ('ś', 's'),

    ('zia', 'za'),
    ('zie', 'ze'),
    ('zio', 'zo'),
    ('ziu', 'zu'),
    ('ź', 'z'),
    ('ż', 'z')
]


def apply_substitution(word: str, substitution: tuple[str, str]) -> str:
    return word.replace(substitution[0], substitution[1])


def normalize(word: str) -> str:
    return reduce(apply_substitution, substitutions, word)
