from collections.abc import Collection, Container, Iterable, Mapping
from string import punctuation
from typing import Optional


class Typo:
    def __init__(self, actual_text: str, correct_text: str, count: int):
        self.actual_text = actual_text
        self.correct_text = correct_text
        self.count = count

    def __str__(self):
        return f'{self.count} times: "{self.actual_text}" instead of "{self.correct_text}"'


class TypoFinder:
    def find(self,
             word_to_frequency: Mapping[str, int],
             bigram_to_frequency: Mapping[tuple[str, str], int]) -> Iterable[Typo]:
        raise NotImplementedError


class MorfologikTypoFinder(TypoFinder):
    def __init__(self, dictionary_path: str):
        self.words = MorfologikTypoFinder.load_words(dictionary_path)

    @staticmethod
    def load_words(path: str) -> Container[str]:
        with open(path, encoding='utf8') as file:
            return set(map(lambda line: line.split(';')[1].lower(), file.readlines()))

    def is_correct_word(self, text: str) -> bool:
        stripped_text = text.strip(punctuation)
        return not stripped_text.isalpha() or stripped_text in self.words

    def get_excessive_space_typo(self,
                                 bigram: tuple[str, str],
                                 frequency: int,
                                 word_to_frequency: Mapping[str, int]) -> Optional[Typo]:
        word = ''.join(bigram)

        if (not self.is_correct_word(bigram[0]) and
                not self.is_correct_word(bigram[1]) and
                word in word_to_frequency and
                word_to_frequency[word] > frequency):
            return Typo(actual_text=' '.join(bigram), correct_text=word, count=frequency)
        else:
            return None

    def find_excessive_spaces(self,
                              word_to_frequency: Mapping[str, int],
                              bigram_to_frequency: Mapping[tuple[str, str], int]) -> tuple[Typo]:
        typos = (self.get_excessive_space_typo(bigram, frequency, word_to_frequency)
                 for bigram, frequency in bigram_to_frequency.items())
        return tuple(typo for typo in typos if typo is not None)

    @staticmethod
    def get_bigrams_for_word(word: str) -> Collection[tuple[str, str]]:
        return tuple((word[:split_index], word[split_index:])
                     for split_index in range(1, len(word) - 1))

    @staticmethod
    def get_most_probable_bigram_for_word(
            word: str,
            bigram_to_frequency: Mapping[tuple[str, str], int]
    ) -> Optional[tuple[str, str]]:
        bigrams = MorfologikTypoFinder.get_bigrams_for_word(word)

        if len(bigrams) == 0:
            return None
        else:
            return max(bigrams,
                       key=lambda bigram: bigram_to_frequency[bigram] if bigram in bigram_to_frequency else 0)

    def get_missing_space_typo(self,
                               word: str,
                               frequency: int,
                               bigram_to_frequency: Mapping[tuple[str, str], int]) -> Optional[Typo]:
        best_bigram = MorfologikTypoFinder.get_most_probable_bigram_for_word(word, bigram_to_frequency)

        if (best_bigram is not None and
                not self.is_correct_word(word) and
                best_bigram in bigram_to_frequency and
                bigram_to_frequency[best_bigram] > frequency):
            return Typo(actual_text=word, correct_text=' '.join(best_bigram), count=frequency)
        else:
            return None

    def find_missing_spaces(self,
                            word_to_frequency: Mapping[str, int],
                            bigram_to_frequency: Mapping[tuple[str, str], int]) -> tuple[Typo]:
        typos = (self.get_missing_space_typo(word, frequency, bigram_to_frequency)
                 for word, frequency in word_to_frequency.items())
        return tuple(typo for typo in typos if typo is not None)

    def find(self,
             word_to_frequency: Mapping[str, int],
             bigram_to_frequency: Mapping[tuple[str, str], int]) -> Iterable[Typo]:
        excessive_spaces = self.find_excessive_spaces(word_to_frequency, bigram_to_frequency)
        missing_spaces = self.find_missing_spaces(word_to_frequency, bigram_to_frequency)
        return sorted(excessive_spaces + missing_spaces, key=lambda typo: typo.count, reverse=True)
