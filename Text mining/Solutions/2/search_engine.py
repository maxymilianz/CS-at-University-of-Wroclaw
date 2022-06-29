from index_manager import FileIndexManager
from lemmatizer import Lemmatizer
from utilities import extract_words
from wikipedia_io import Article, WikipediaIo

from functools import reduce
from operator import and_, or_
from typing import Iterable


class MatchRating:
    def __init__(self, article_count: int, lemmatizer: Lemmatizer):
        self.article_count = article_count
        self.lemmatizer = lemmatizer

    def rate_article_id(self, id: int) -> float:
        return (self.article_count - id) / self.article_count

    @staticmethod
    def count_common_words(words_0: Iterable[str], words_1: Iterable[str]) -> int:
        return len(tuple(word for word in words_0 if word in words_1))

    def rate_text_suitability(self, text: str, query: str) -> float:
        text_words = extract_words(text)
        query_words = extract_words(query)
        exact_words_score = MatchRating.count_common_words(text_words, query_words)

        text_lemmas = reduce(or_, (self.lemmatizer.lemmatize(word) for word in text_words), set())
        query_lemmas = reduce(or_, (self.lemmatizer.lemmatize(word) for word in query_words), set())
        lemmas_score = MatchRating.count_common_words(text_lemmas, query_lemmas)

        return 2*exact_words_score + lemmas_score

    def rate(self, article: Article, query: str) -> float:
        id_score = self.rate_article_id(article.id)
        title_score = self.rate_text_suitability(article.title, query)
        contents_score = self.rate_text_suitability(article.contents, query)
        return 10*id_score + title_score + 0 * contents_score


class SearchEngine:
    def __init__(self, lemmatizer: Lemmatizer,
                 index_manager: FileIndexManager,
                 wikipedia_io: WikipediaIo,
                 match_rating: MatchRating):
        self.lemmatizer = lemmatizer
        self.index_manager = index_manager
        self.wikipedia_io = wikipedia_io
        self.match_rating = match_rating

    def get_article_ids(self, query: str) -> Iterable[int]:
        # Incorrect, because if e.g. user looks for "mam", in each article there must be both a word for lemma "mieć" and "mama".
        lemmas = self.lemmatizer.get_lemmas_for_text(query)
        return (() if len(lemmas) == 0
                else reduce(and_, map(self.index_manager.get_posting_list, lemmas)).document_ids)

    def get_articles(self, query: str) -> Iterable[Article]:
        article_ids = self.get_article_ids(query)
        return map(self.wikipedia_io.find_article, article_ids)

    def sort_articles(self, articles: Iterable[Article], query: str) -> Iterable[Article]:
        return sorted(articles, key=lambda article: self.match_rating.rate(article, query), reverse=True)

    def search(self, query: str) -> Iterable[Article]:
        articles = self.get_articles(query)
        return self.sort_articles(articles, query)
