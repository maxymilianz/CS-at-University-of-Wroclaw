from definition import Definition
from lemmatizer import Lemmatizer
from similar_definition_finder.similar_definition_finder import SimilarDefinitionFinder
from utilities import extract_words

from collections import defaultdict
from collections.abc import Collection, Iterable, Mapping, Sequence
from functools import reduce
from gensim.models import KeyedVectors
from math import inf
from numpy import log2, ndarray, ones, zeros_like
from operator import or_
from scipy.spatial import distance


class CosineEmbeddingSimilarDefinitionFinder(SimilarDefinitionFinder):
    def __init__(self,
                 lemmatizer: Lemmatizer,
                 definitions: Collection[Definition],
                 word2vec_path: str):
        self.lemmatizer = lemmatizer

        self.lemma_to_articles = defaultdict(set)

        print('Lemmatizing definitions.')
        lemmatized_definitions = set(map(self.lemmatize_definition, definitions))
        self.name_to_definition = CosineEmbeddingSimilarDefinitionFinder.get_name_to_definition(lemmatized_definitions)

        print('Loading word2vec.')
        self.word2vec = KeyedVectors.load(word2vec_path)

        print('Computing lemma -> position in one-hot vectors.')
        self.lemma_to_position = self.get_lemma_to_position()

        self.inverse_document_frequencies = self.get_inverse_document_frequencies()

        print('Computing name -> vector.')
        self.name_to_vector = self.get_name_to_vector(lemmatized_definitions)

    def lemmatize(self, word: str) -> str:
        lemmas = self.lemmatizer.lemmatize(word)
        return (word if len(lemmas) == 0
                else min(self.lemmatizer.lemmatize(word)))  # Arbitrarily yet deterministically choose one lemma.

    def lemmatize_definition(self, definition: Definition) -> Definition:
        name_words = extract_words(definition.name)
        lemmatized_name = ' '.join(map(self.lemmatize, name_words))

        description_words = extract_words(definition.description)
        lemmatized_description = ' '.join(map(self.lemmatize, description_words))

        return Definition(lemmatized_name, lemmatized_description)

    @staticmethod
    def get_name_to_definition(definitions: Collection[Definition]) -> Mapping[str, Definition]:
        return {definition.name: definition for definition in definitions}

    @staticmethod
    def get_words_for_definition(definition: Definition) -> set[str]:
        return set(extract_words(definition.description))

    def get_lemma_to_position(self) -> Mapping[str, int]:
        lemma_sets = map(CosineEmbeddingSimilarDefinitionFinder.get_words_for_definition,
                         self.name_to_definition.values())
        lemmas = reduce(or_, lemma_sets)
        return {lemma: position
                for position, lemma in enumerate(sorted(lemmas))}

    def get_lemma_definition_counts(self) -> ndarray:
        lemma_definition_counts = ones(len(self.lemma_to_position))  # Should be 0s.

        for definition in self.name_to_definition.values():
            for lemma in self.get_words_for_definition(definition):
                self.lemma_to_articles[lemma].add(definition)
                lemma_definition_counts[self.lemma_to_position[lemma]] += 1

        return lemma_definition_counts

    def get_inverse_document_frequencies(self) -> ndarray:
        definition_count = len(self.name_to_definition)
        lemma_definition_counts = self.get_lemma_definition_counts()
        return log2(definition_count / lemma_definition_counts)

    def get_word_embedding(self, word: str) -> ndarray:
        return (self.word2vec[word] if word in self.word2vec
                else zeros_like(self.word2vec['a']))

    def get_description_vector(self, description: str) -> ndarray:
        words = extract_words(description)

        if len(words) == 0:
            return zeros_like(self.word2vec['a'])
        else:
            lemmas = map(self.lemmatize, words)
            result = zeros_like(self.word2vec['a'])

            for lemma in lemmas:
                embedding = self.get_word_embedding(lemma)

                if lemma in self.lemma_to_position:
                    result += embedding * self.inverse_document_frequencies[self.lemma_to_position[lemma]]

            return result

    def get_name_to_vector(self, definitions: Collection[Definition]) -> Mapping[str, ndarray]:
        return {definition.name: self.get_description_vector(definition.description)
                for definition in definitions}

    def distance(self, name: str, desired_vector: ndarray) -> float:
        vector = self.name_to_vector[name]
        # return (inf if all(element == 0 for element in vector)
        #         else distance.cosine(vector, desired_vector))
        return distance.cosine(vector, desired_vector)

    def get_possible_definitions(self, description: str) -> Iterable[Definition]:
        words = extract_words(description)
        lemmas = set(map(self.lemmatize, words))

        if len(lemmas) == 0:
            return self.name_to_definition.values()
        else:
            rarest_lemma = min(lemmas, key=lambda lemma: len(self.lemma_to_articles[lemma]))
            return self.lemma_to_articles[rarest_lemma]

    def get_similar_definitions(self, description: str) -> Sequence[Definition]:
        description_vector = self.get_description_vector(description)
        definitions = set(self.get_possible_definitions(description))
        return sorted(definitions,
                      key=lambda definition: self.distance(definition.name, description_vector))
