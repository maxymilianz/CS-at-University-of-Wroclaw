from nltk.tokenize import word_tokenize
from spacy.lang.pl import Polish
from string import punctuation
from typing import Iterable


def load_quotes(path: str) -> Iterable[str]:
    with open(path, encoding='utf8') as file:
        return [quote.strip()[2:] for quote in file.readlines()]


def strip_punctuation(word: str) -> str:
    return word.strip(punctuation)


def tokenize_line(line: str) -> Iterable[str]:
    return filter(lambda word: len(word) > 0, map(strip_punctuation, line.split()))


def tokenize(lines: Iterable[str]) -> Iterable[Iterable[str]]:
    return map(tokenize_line, lines)


def nltk_tokenize(lines: Iterable[str]) -> Iterable[Iterable[str]]:
    return [word_tokenize(line) for line in lines]


# https://spacy.io/api/tokenizer
def spacy_tokenize(lines: Iterable[str]) -> Iterable[Iterable[str]]:
    tokenizer = Polish().tokenizer
    return [map(str, tokenizer(line)) for line in lines]


def compare_line_tokenizations(tokenization_0: Iterable[str], tokenization_1: Iterable[str]) -> Iterable[str]:
    return set(tokenization_0).symmetric_difference(set(tokenization_1))


def compare_tokenizations(tokenization_0: Iterable[Iterable[str]],
                          tokenization_1: Iterable[Iterable[str]]) -> Iterable[Iterable[str]]:
    return [compare_line_tokenizations(line_tokenization_0, line_tokenization_1)
            for line_tokenization_0, line_tokenization_1 in zip(tokenization_0, tokenization_1)]


def tokenization_to_string(tokenization: Iterable[Iterable[str]]) -> str:
    return '\n'.join(' '.join(line_tokenization) for line_tokenization in tokenization)


def write_to_file(contents: str, path: str):
    with open(path, 'w', encoding='utf8') as file:
        file.write(contents)


def main():
    quotes = load_quotes('cytaty.txt')

    # tokenization = tokenize(quotes)
    # nltk_tokenization = nltk_tokenize(quotes)
    # spacy_tokenization = spacy_tokenize(quotes)
    # tokenization_difference = compare_tokenizations(tokenization, nltk_tokenization)

    # write_to_file(tokenization_to_string(tokenization), '3 - tokenization.txt')
    # write_to_file(tokenization_to_string(nltk_tokenization), '3 - nltk tokenization.txt')
    # write_to_file(tokenization_to_string(spacy_tokenization), '3 - spacy tokenization.txt')
    # write_to_file(tokenization_to_string(tokenization_difference), '3 - tokenization comparison.txt')


if __name__ == '__main__':
    main()
