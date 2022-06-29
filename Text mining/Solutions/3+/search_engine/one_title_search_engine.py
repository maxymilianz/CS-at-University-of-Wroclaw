from search_engine.abstract_search_engine import AbstractSearchEngine
from wikipedia_io import Article

from collections.abc import Collection, Iterable


class OneTitleSearchEngine(AbstractSearchEngine):
    def __init__(self, articles: Iterable[Article]):
        self.articles = set(articles)

    def get_articles_for_query(self, query: str) -> Collection[Article]:
        return {article for article in self.articles if query in article.title.lower()}

    @staticmethod
    def get_title_length(title: str) -> int:
        parenthesis_index = title.find('(')
        return (len(title) if parenthesis_index == -1
                else parenthesis_index)

    @staticmethod
    def are_titles_same(title_0: str, title_1: str) -> bool:
        parenthesis_index_0 = title_0.find('(')
        parenthesis_index_1 = title_1.find('(')

        return ((title_0 if parenthesis_index_0 == 0 else title_0[:parenthesis_index_0]) ==
                (title_1 if parenthesis_index_1 == 0 else title_1[:parenthesis_index_1]))

    @staticmethod
    def filter_articles(articles: Collection[Article]) -> Iterable[Article]:
        article_to_title_length = {article: OneTitleSearchEngine.get_title_length(article.title)
                                   for article in articles}
        min_title_length = min(article_to_title_length.values())
        shortest_title_articles = {article for article, title_length in article_to_title_length.items()
                                   if title_length == min_title_length}

        min_id_article = min(shortest_title_articles, key=lambda article: article.id)
        return (article for article in shortest_title_articles
                if OneTitleSearchEngine.are_titles_same(min_id_article.title, article.title))

    def search(self, query: str) -> Iterable[Article]:
        articles = self.get_articles_for_query(query)
        return OneTitleSearchEngine.filter_articles(articles)

    def idf(self, term: str) -> float:
        raise NotImplementedError
