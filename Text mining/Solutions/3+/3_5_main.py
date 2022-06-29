from default_object_factories import get_morfologik_typo_finder
from typo_finder import Typo

from collections.abc import Iterable, Mapping


def parse_1_gram(text: str) -> tuple[str, int]:
    frequency, word = text.split()
    return word, int(frequency)


def load_1_grams(path: str) -> Mapping[str, int]:
    with open(path, encoding='utf8') as file:
        return {word: frequency for word, frequency in map(parse_1_gram, file.readlines())}


def parse_2_gram(text: str) -> tuple[tuple[str, str], int]:
    frequency, word_0, word_1 = text.split()
    return (word_0, word_1), int(frequency)


def load_2_grams(path: str) -> Mapping[tuple[str, str], int]:
    with open(path, encoding='utf8') as file:
        return {words: frequency for words, frequency in map(parse_2_gram, file.readlines())}


def save_typos_to_file(typos: Iterable[Typo], path: str):
    with open(path, 'w+', encoding='utf8') as file:
        for typo in typos:
            file.write(f'{typo}\n')


def main():
    print('Loading 1-grams.')
    one_grams = load_1_grams('resources/1grams')

    print('Loading 2-grams.')
    two_grams = load_2_grams('resources/2grams')

    print('Loading typo finder.')
    typo_finder = get_morfologik_typo_finder()

    print('Looking for typos.')
    typos = typo_finder.find(one_grams, two_grams)

    print('Saving typos.')
    save_typos_to_file(typos, 'resources/typos.txt')


if __name__ == '__main__':
    main()
