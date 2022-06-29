from wikipedia_io import Article

from typing import Iterable


class AbstractArticlePresenter:
    def present(self, articles: Iterable[Article], query: str):
        raise NotImplementedError
