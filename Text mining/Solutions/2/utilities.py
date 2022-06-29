import editdistance
from string import punctuation
from typing import Iterable, Sequence, TypeVar


quote_prefix = '* '


def clean_quote(quote: str) -> str:
    return quote.strip()[len(quote_prefix):]


def load_quotes(path: str) -> Sequence[str]:
    with open(path, encoding='utf8') as file:
        return tuple(clean_quote(quote) for quote in file.readlines())


def quotes_to_string(quotes: Iterable[str]) -> str:
    return quote_prefix + f'\n{quote_prefix}'.join(quotes)


T = TypeVar('T')
U = TypeVar('U')


def unzip(values: Iterable[tuple[T, U]]) -> tuple[Sequence[T], Sequence[U]]:
    ts, us = (), ()

    for t, u in values:
        ts += t,
        us += u,

    return ts, us


def extract_words(text: str) -> Sequence[str]:
    return tuple(word.strip(punctuation) for word in text.split())


def scaled_edit_distance(text: str, correct_text: str) -> float:
    return editdistance.eval(text, correct_text) / len(correct_text)


def write_to_file(contents: str, path: str):
    with open(path, 'w', encoding='utf8') as file:
        file.write(contents)
