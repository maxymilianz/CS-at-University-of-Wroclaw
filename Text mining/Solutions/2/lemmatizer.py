from utilities import extract_words

from collections import defaultdict
from functools import reduce
from operator import or_


class Lemmatizer:
    def lemmatize(self, word: str) -> set[str]:
        raise NotImplementedError

    def get_lemmas_for_text(self, text: str) -> set[str]:
        raise NotImplementedError


class MorfologikLemmatizer(Lemmatizer):
    def __init__(self, lemmas_path: str):
        self.word_to_lemmas = MorfologikLemmatizer.load_lemmas(lemmas_path)

    @staticmethod
    def load_lemmas(path: str) -> dict[str, set[str]]:
        word_to_lemmas = defaultdict(set)

        with open(path, encoding='utf8') as file:
            for line in file.readlines():
                lemma, word, _ = line.split(';')
                word_to_lemmas[word.lower()].add(lemma.lower())

        return word_to_lemmas

    def lemmatize(self, word: str) -> set[str]:
        lowercase_word = word.lower()

        if lowercase_word in self.word_to_lemmas:
            return self.word_to_lemmas[lowercase_word]
        else:
            return {lowercase_word} if word.isalpha() else set()

    def get_lemmas_for_text(self, text: str) -> set[str]:
        lemma_sets = (self.lemmatize(word) for word in extract_words(text))
        return reduce(or_, lemma_sets, set())
