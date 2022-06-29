from definition import Definition
from lemmatizer import Lemmatizer
from similar_definition_finder.similar_definition_finder import SimilarDefinitionFinder
from utilities import extract_words

from collections.abc import Collection, Iterable, Mapping, Sequence
from functools import reduce
from numpy import array, log2, ndarray
from operator import or_
from scipy.spatial import distance


class CosineTfIdfSimilarDefinitionFinder(SimilarDefinitionFinder):
    def __init__(self, lemmatizer: Lemmatizer, definitions: Collection[Definition]):
        self.lemmatizer = lemmatizer

        self.name_to_definition = CosineTfIdfSimilarDefinitionFinder.get_name_to_definition(definitions)

        print('Computing lemma -> position in one-hot vectors.')
        self.lemma_to_position = self.get_lemma_to_position(definitions)

        self.inverse_document_frequencies = self.get_inverse_document_frequencies()

        print('Computing name -> vector.')
        self.name_to_vector = self.get_name_to_vector(definitions)

    @staticmethod
    def get_name_to_definition(definitions: Collection[Definition]) -> Mapping[str, Definition]:
        return {definition.name: definition for definition in definitions}

    def get_lemmas_for_definition(self, definition: Definition) -> set[str]:
        return self.lemmatizer.get_lemmas_for_text(definition.description)

    def get_lemma_to_position(self, definitions: Collection[Definition]) -> Mapping[str, int]:
        lemma_sets = map(self.get_lemmas_for_definition, definitions)
        lemmas = reduce(or_, lemma_sets)
        return {lemma: position
                for position, lemma in enumerate(sorted(lemmas))}

    def get_lemma_definition_counts(self) -> ndarray:
        lemma_definition_counts = array([1 for _ in self.lemma_to_position])  # Should be 0.

        for definition in self.name_to_definition.values():
            for lemma in self.get_lemmas_for_definition(definition):
                lemma_definition_counts[self.lemma_to_position[lemma]] += 1

        return lemma_definition_counts

    def get_inverse_document_frequencies(self) -> ndarray:
        definition_count = len(self.name_to_definition)
        lemma_definition_counts = self.get_lemma_definition_counts()
        return log2(definition_count / lemma_definition_counts)

    def get_term_frequencies(self, description: str) -> ndarray:
        words = extract_words(description)
        lemma_sets = tuple(map(self.lemmatizer.lemmatize, words))

        term_count = sum(map(len, lemma_sets))
        term_occurrence_counts = array([0 for _ in self.lemma_to_position])

        for lemmas in lemma_sets:
            for lemma in lemmas:
                if lemma in self.lemma_to_position:
                    # There may be some strange words in questions, but not in definitions.
                    term_occurrence_counts[self.lemma_to_position[lemma]] += 1

        return (term_occurrence_counts / term_count if term_count != 0
                else term_occurrence_counts)  # term_occurrence_counts == [0, ..., 0]

    def get_description_vector(self, description: str) -> ndarray:
        return self.get_term_frequencies(description) * self.inverse_document_frequencies

    def get_name_to_vector(self, definitions: Collection[Definition]) -> Mapping[str, ndarray]:
        return {definition.name: self.get_description_vector(definition.description)
                for definition in definitions}

    # Returns way too many vectors, so the program runs in ~10 minutes instead of 1s XD
    @staticmethod
    def are_vectors_perpendicular(vector_0: ndarray, vector_1: ndarray) -> bool:
        return all(element_0 == 0 or element_1 == 0
                   for element_0, element_1 in zip(vector_0, vector_1))

    def get_highest_idf_indexes(self, description_vector: ndarray) -> Sequence[int]:
        return sorted((index for index, element in enumerate(description_vector) if element > 0.00001),
                      key=lambda index: self.inverse_document_frequencies[index],
                      reverse=True)

    def get_possible_definitions(self, description_vector: ndarray) -> Iterable[Definition]:
        highest_idf_lemma_indexes = self.get_highest_idf_indexes(description_vector)[:2]
        print(f'Highest idf lemma: {[lemma for lemma, position in self.lemma_to_position.items() if position == highest_idf_lemma_indexes[0]]}.')
        return (self.name_to_definition[name]
                for name, vector in self.name_to_vector.items()
                if any(vector[index] != 0 for index in highest_idf_lemma_indexes))

    def get_similar_definitions(self, description: str) -> Sequence[Definition]:
        print(f'Computing description vector for "{description}".')
        description_vector = self.get_description_vector(description)
        print('Retrieving possible definitions.')
        definitions = set(self.get_possible_definitions(description_vector))
        print(f'There are {len(definitions)} possible definitions.')
        return sorted(definitions,
                      key=lambda definition: distance.cosine(self.name_to_vector[definition.name], description_vector))
