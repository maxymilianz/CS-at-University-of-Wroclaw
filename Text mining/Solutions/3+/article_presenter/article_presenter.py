from article_presenter.abstract_article_presenter import AbstractArticlePresenter
from lemmatizer import Lemmatizer
from wikipedia_io import Article

import colorama
from typing import Iterable


class ArticlePresenter(AbstractArticlePresenter):
    def __init__(self, lemmatizer: Lemmatizer):
        self.lemmatizer = lemmatizer

    def process_word(self, word: str, emphasized_lemmas: set[str]) -> str:
        if self.lemmatizer.lemmatize(word).isdisjoint(emphasized_lemmas):
            return word
        else:
            return f'{colorama.Fore.GREEN}{word}{colorama.Fore.RESET}'

    def process_title(self, title: str, emphasized_lemmas: set[str]) -> str:
        processed_words = (self.process_word(word, emphasized_lemmas)
                           for word in title.split())
        return f'{colorama.Style.BRIGHT}{" ".join(processed_words)}{colorama.Style.RESET_ALL}'

    def get_desired_word_indexes(self, words: Iterable[str], emphasized_lemmas: set[str]) -> set[int]:
        return {index for index, word in enumerate(words)
                if not self.lemmatizer.lemmatize(word).isdisjoint(emphasized_lemmas)}

    def get_matching_snippets(self, contents: str, emphasized_lemmas: set[str]) -> Iterable[str]:
        words = contents.split()
        desired_word_indexes = self.get_desired_word_indexes(words, emphasized_lemmas)
        snippets = []
        snippet_words = []

        for index, word in enumerate(words):
            if desired_word_indexes.isdisjoint({index - 2, index - 1, index, index + 1, index + 2}):
                if len(snippet_words) != 0:
                    snippets.append(' '.join(snippet_words))
                    snippet_words = []
            else:
                snippet_words.append(self.process_word(word, emphasized_lemmas))

        return snippets

    def process_contents(self, contents: str, emphasized_lemmas: set[str]) -> str:
        snippets = self.get_matching_snippets(contents, emphasized_lemmas)
        return ' ... '.join(snippets)

    def article_to_string(self, article: Article, emphasized_lemmas: set[str]) -> str:
        title = self.process_title(article.title, emphasized_lemmas)
        contents = self.process_contents(article.contents, emphasized_lemmas)
        return (f'{title}\n'
                f'{contents}')

    def present(self, articles: Iterable[Article], query: str):
        lemmas = self.lemmatizer.get_lemmas_for_text(query)

        for article in articles:
            print(self.article_to_string(article, lemmas))
            print()
