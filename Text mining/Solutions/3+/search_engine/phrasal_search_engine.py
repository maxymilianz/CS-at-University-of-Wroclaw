from index_manager.abstract_index_manager import IndexManager
from lemmatizer import Lemmatizer
from position_to_article_mapper import PositionToArticleMapper
from search_engine.abstract_search_engine import AbstractSearchEngine
from utilities import extract_words
from wikipedia_io import Article, WikipediaIo

from collections.abc import Iterable
from functools import cache, reduce
from itertools import product
from math import inf, log
from operator import or_


class Phrase:
    def __init__(self, words: Iterable[str]):
        self.words = words

    def __str__(self):
        return ' '.join(self.words)


class PhrasalSearchEngine(AbstractSearchEngine):
    def __init__(self,
                 lemmatizer: Lemmatizer,
                 positional_index_manager: IndexManager,
                 position_to_article_mapper: PositionToArticleMapper,
                 wikipedia_io: WikipediaIo):
        self.lemmatizer = lemmatizer
        self.positional_index_manager = positional_index_manager
        self.position_to_article_mapper = position_to_article_mapper
        self.wikipedia_io = wikipedia_io

    def get_lemmatized_phrases(self, query: str) -> Iterable[Phrase]:
        words = extract_words(query)
        lemma_sets = map(self.lemmatizer.lemmatize, words)
        return map(Phrase, product(*lemma_sets))

    def get_positions_for_whole_phrase(self, phrase: Phrase) -> Iterable[int]:
        position_sets = [self.positional_index_manager.get_posting_list({word}) for word in phrase.words]

        return reduce(lambda later_word_positions, earlier_word_positions: set(
            filter(lambda position: position + 1 in later_word_positions,
                   earlier_word_positions)
        ), reversed(position_sets))

    def get_articles_for_phrase(self, phrase: Phrase) -> set[Article]:
        positions = self.get_positions_for_whole_phrase(phrase)
        article_ids = map(self.position_to_article_mapper.get_article_id_for_position, positions)
        return set(map(self.wikipedia_io.find_article, article_ids))

    def search(self, query: str) -> Iterable[Article]:
        lemmatized_phrases = self.get_lemmatized_phrases(query)
        article_sets = map(self.get_articles_for_phrase, lemmatized_phrases)
        return reduce(or_, article_sets, set())

    def count_articles_for_word(self, word: str) -> int:
        lemmas = self.lemmatizer.lemmatize(word)
        positions = self.positional_index_manager.get_posting_list(lemmas)
        article_ids = map(self.position_to_article_mapper.get_article_id_for_position, positions)
        return len(set(article_ids))

    @cache
    def idf(self, term: str) -> float:
        article_count = self.wikipedia_io.get_last_article_id()
        desired_article_count = self.count_articles_for_word(term)
        return (inf if desired_article_count == 0
                else log(article_count / desired_article_count))
