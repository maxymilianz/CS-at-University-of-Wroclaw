from lemmatizer import Lemmatizer
from wikipedia_io import Article

import colorama
from typing import Iterable


class ArticlePresenter:
    def __init__(self, lemmatizer: Lemmatizer):
        self.lemmatizer = lemmatizer

    def process_word(self, word: str, emphasized_lemmas: set[str]) -> str:
        if len(self.lemmatizer.lemmatize(word).intersection(emphasized_lemmas)) == 0:
            return word
        else:
            return f'{colorama.Fore.GREEN}{word}{colorama.Fore.RESET}'

    def process_title(self, title: str, emphasized_lemmas: set[str]) -> str:
        return ' '.join(self.process_word(word, emphasized_lemmas)
                        for word in title.split())

    def get_desired_word_indexes(self, words: Iterable[str], emphasized_lemmas: set[str]) -> Iterable[int]:
        indexes = set()

        for index, word in enumerate(words):
            if len(self.lemmatizer.lemmatize(word).intersection(emphasized_lemmas)) != 0:
                indexes.update({index - 2, index - 1, index, index + 1, index + 2})

        return indexes

    def get_matching_snippets(self, contents: str, emphasized_lemmas: set[str]) -> Iterable[str]:
        words = contents.split()
        desired_word_indexes = self.get_desired_word_indexes(words, emphasized_lemmas)
        snippets = []
        snippet_words = []

        for index, word in enumerate(words):
            if index in desired_word_indexes:
                snippet_words.append(self.process_word(word, emphasized_lemmas))
            else:
                if len(snippet_words) != 0:
                    snippets.append(' '.join(snippet_words))
                    snippet_words = []

        return snippets

    def process_contents(self, contents: str, emphasized_lemmas: set[str]) -> str:
        snippets = self.get_matching_snippets(contents, emphasized_lemmas)
        return ' ... '.join(snippets)

    def article_to_string(self, article: Article, emphasized_lemmas: set[str]) -> str:
        title = self.process_title(article.title, emphasized_lemmas)
        contents = self.process_contents(article.contents, emphasized_lemmas)
        return (f'{colorama.Style.BRIGHT}{title}{colorama.Style.RESET_ALL}\n'
                f'{contents}')

    def present(self, articles: Iterable[Article], query: str):
        lemmas = self.lemmatizer.get_lemmas_for_text(query)

        for article in articles:
            print(self.article_to_string(article, lemmas))
            print()
