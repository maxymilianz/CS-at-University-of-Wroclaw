from lemmatizer import Lemmatizer

from collections import defaultdict
from functools import reduce
from operator import or_
from typing import Iterable


class Inflector:
    def inflect(self, word: str) -> Iterable[str]:
        raise NotImplementedError


class MorfologikInflector(Inflector):
    def __init__(self, inflections_path: str, lemmatizer: Lemmatizer):
        self.lemma_to_inflections = MorfologikInflector.load_inflections(inflections_path)
        self.lemmatizer = lemmatizer

    @staticmethod
    def load_inflections(path: str) -> dict[str, set[str]]:
        word_to_inflections = defaultdict(set)

        with open(path, encoding='utf8') as file:
            for line in file.readlines():
                lemma, word, _ = line.split(';')
                word_to_inflections[lemma.lower()].add(word.lower())

        return word_to_inflections

    def inflect(self, word: str) -> Iterable[str]:
        lemmas = self.lemmatizer.lemmatize(word)
        inflection_sets = (self.lemma_to_inflections[lemma] for lemma in lemmas)
        return reduce(or_, inflection_sets, set())
