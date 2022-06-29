from wikipedia_io import Article

from collections.abc import Iterable


class AbstractSearchEngine:
    def search(self, query: str) -> Iterable[Article]:
        raise NotImplementedError

    def idf(self, term: str) -> float:
        raise NotImplementedError
