from corrector.corrector import Corrector, Typo
from default_object_factories import get_corrector, WordSource

from collections.abc import Sequence


def parse_typo(text: str) -> Typo:
    correct_word, actual_word = text.split()
    return Typo(actual_word=actual_word, correct_word=correct_word)


def load_typos(path: str) -> Sequence[Typo]:
    with open(path, encoding='utf8') as file:
        return tuple(map(parse_typo, file.readlines()))


class Logger:
    def __init__(self, log_path: str):
        self.log_path = log_path

        with open(log_path, 'w+') as file:
            file.write('')

    def log(self, text: str):
        print(text)

        with open(self.log_path, 'a+', encoding='utf8') as file:
            file.write(f'{text}\n')


def correct_typos(typos: Sequence[Typo], corrector: Corrector, logger: Logger):
    correct_correction_count = 0

    for typo in typos:
        correction = corrector.correct(typo.actual_word)

        if correction == typo.correct_word:
            correct_correction_count += 1
        else:
            incorrect_correction = f'"{typo.actual_word}" corrected to "{correction}" instead of "{typo.correct_word}"'
            logger.log(incorrect_correction)

    print()
    print(f'{correct_correction_count / len(typos) * 100}% of typos corrected correctly')


def main():
    typos = load_typos('resources/literowki1.txt')
    corrector = get_corrector(WordSource.MORFOLOGIK)
    logger = Logger('resources/3.6 - test log.txt')
    correct_typos(typos, corrector, logger)


if __name__ == '__main__':
    main()
