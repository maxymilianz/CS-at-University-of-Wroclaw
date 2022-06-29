from corrector.corrector import Corrector
from edit_distance import edit_distance

from collections import defaultdict
from collections.abc import Iterable, Mapping
from editdistance import distance
from functools import reduce
from operator import or_
from typing import Optional
from unidecode import unidecode


class SluggyCorrector(Corrector):
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
                            'm': 'njk',

                            ' ': 'cvbnm'}

    def __init__(self, words: Iterable[str]):
        self.letter_to_words = SluggyCorrector.load_letter_to_words(words)
        self.normalized_to_denormalized = self.get_normalized_to_denormalized()

    @staticmethod
    def load_letter_to_words(words: Iterable[str]) -> Mapping[str, set[str]]:
        letter_to_words = defaultdict(set)

        for word in words:
            lowercase_word = word.lower()
            letter_to_words[lowercase_word[0]].add(lowercase_word)

        return letter_to_words

    @staticmethod
    def normalize(word: str) -> str:
        return unidecode(word)

    def get_normalized_to_denormalized(self) -> Mapping[str, set[str]]:
        normalized_to_denormalized = defaultdict(set)

        for word_set in self.letter_to_words.values():
            for word in word_set:
                depolonized = SluggyCorrector.normalize(word)
                normalized_to_denormalized[depolonized].add(word)

        return normalized_to_denormalized

    @staticmethod
    def distance(word_0: str, word_1: str) -> float:
        return distance(word_0, word_1)
        # return edit_distance(word_0, word_1)

    def correct_with_same_normalization(self, word: str) -> Optional[str]:
        possible_corrections = self.normalized_to_denormalized[SluggyCorrector.normalize(word)]

        if len(possible_corrections) == 0:
            return None
        else:
            return min(possible_corrections, key=lambda polonization: SluggyCorrector.distance(word, polonization))

    @staticmethod
    def remove_one_letter(word: str) -> set[str]:
        return {word[:i] + word[i + 1:] for i in range(len(word) - 1)}

    @staticmethod
    def add_one_letter(word: str) -> set[str]:
        # return {word[:i] + letter + word[i:]
        #         for i in range(len(word))
        #         for letter in MorfologikCorrector.letter_to_neighbours.keys()}
        return {word[:i] + letter + word[i:]
                for i in range(len(word) + 1)
                for letter in ((SluggyCorrector.letter_to_neighbours[word[i - 1]] if i >= 1
                                else '') +
                               (SluggyCorrector.letter_to_neighbours[word[i]] if i < len(word)
                                else ''))}

    @staticmethod
    def misspell_one_letter(word: str) -> set[str]:
        return {word[:i] + letter + word[i + 1:]
                for i in range(len(word) - 1)
                for letter in SluggyCorrector.letter_to_neighbours[word[i]]}

    @staticmethod
    def swap_adjacent_letters(word: str) -> set[str]:
        return {word[:i] + word[i + 1] + word[i] + word[i + 2:]
                for i in range(len(word) - 1)}

    @staticmethod
    def add_one_typo(word: str) -> Iterable[str]:
        return (SluggyCorrector.remove_one_letter(word) |
                SluggyCorrector.add_one_letter(word) |
                SluggyCorrector.misspell_one_letter(word) |
                SluggyCorrector.swap_adjacent_letters(word))

    def correct_with_similar_normalization(self, word: str) -> Optional[str]:
        normalization = SluggyCorrector.normalize(word)
        similar_normalization_to_denormalized = {normalization: self.normalized_to_denormalized[normalization]
                                                 for normalization in SluggyCorrector.add_one_typo(normalization)
                                                 if len(self.normalized_to_denormalized[normalization]) != 0}

        if len(similar_normalization_to_denormalized) == 0:
            return None
        else:
            return min(min(denormalized_forms,
                           key=lambda denormalized: SluggyCorrector.distance(normalized, denormalized))
                       for normalized, denormalized_forms in similar_normalization_to_denormalized.items())

    def correct_with_smallest_distance_for_nearby_first_letter(self, word: str) -> str:
        possible_corrections = reduce(or_,
                                      (self.letter_to_words[letter]
                                       for letter in SluggyCorrector.letter_to_neighbours[word[0]]),
                                      self.letter_to_words[word[0]])
        return min(possible_corrections, key=lambda correct_word: SluggyCorrector.distance(word, correct_word))

    def correct(self, word: str) -> str:
        for function in (self.correct_with_same_normalization,
                         self.correct_with_similar_normalization):
            correction = function(word)

            if correction is not None:
                return correction

        return self.correct_with_smallest_distance_for_nearby_first_letter(word)
