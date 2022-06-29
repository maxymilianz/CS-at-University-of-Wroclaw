from utilities import load_quotes, quotes_to_string, write_to_file

import re
from typing import Iterable


def split_quote(quote: str) -> tuple[str]:
    if len(quote) < 200:
        return quote,
    else:
        return tuple(str(sentence) for sentence in re.split('[.;?!]', quote) if len(sentence) > 0)


def split_big_quotes(quotes: Iterable[str]) -> Iterable[str]:
    return sum((split_quote(quote) for quote in quotes), ())


def main():
    quotes = load_quotes('cytaty.txt')
    mini_quotes = split_big_quotes(quotes)
    write_to_file(quotes_to_string(mini_quotes), 'mini_quotes.txt')


if __name__ == '__main__':
    main()
