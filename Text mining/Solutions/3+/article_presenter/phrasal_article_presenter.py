from article_presenter.abstract_article_presenter import AbstractArticlePresenter
from lemmatizer import Lemmatizer
from utilities import extract_words
from wikipedia_io import Article

import colorama
from collections.abc import Iterable, Sequence


class PhrasalArticlePresenter(AbstractArticlePresenter):
    def __init__(self, lemmatizer: Lemmatizer):
        self.lemmatizer = lemmatizer

    def get_consecutive_lemma_sets(self, query: str) -> Sequence[set[str]]:
        words = extract_words(query)
        return tuple(map(self.lemmatizer.lemmatize, words))

    @staticmethod
    def emphasize(word: str) -> str:
        return f'{colorama.Fore.GREEN}{word}{colorama.Fore.RESET}'

    def get_desired_word_indexes(self, words: Sequence[str], consecutive_lemma_sets: Sequence[set[str]]) -> set[int]:
        word_index = 0
        phrase_index = 0
        potential_phrase_indexes = set()
        result = set()

        while word_index < len(words):
            lemmas = self.lemmatizer.lemmatize(words[word_index])

            if len(potential_phrase_indexes) == len(consecutive_lemma_sets):  # found whole phrase
                result.update(potential_phrase_indexes)
                potential_phrase_indexes.clear()
                phrase_index = 0
            elif not lemmas.isdisjoint(consecutive_lemma_sets[phrase_index]):  # found next word from phrase
                potential_phrase_indexes.add(word_index)
                phrase_index += 1
            else:  # word not from phrase
                potential_phrase_indexes.clear()
                phrase_index = 0

            word_index += 1

        return result

    def process_title(self, title: str, consecutive_lemma_sets: Sequence[set[str]]) -> str:
        words = title.split()
        desired_word_indexes = self.get_desired_word_indexes(words, consecutive_lemma_sets)
        processed_words = (PhrasalArticlePresenter.emphasize(word) if index in desired_word_indexes else word
                           for index, word in enumerate(words))
        return f'{colorama.Style.BRIGHT}{" ".join(processed_words)}{colorama.Style.RESET_ALL}'

    def get_matching_snippets(self, contents: str, consecutive_lemma_sets: Sequence[set[str]]) -> Iterable[str]:
        words = contents.split()
        desired_word_indexes = self.get_desired_word_indexes(words, consecutive_lemma_sets)
        snippets = []
        snippet_words = []

        for index, word in enumerate(words):
            if index in desired_word_indexes:
                snippet_words.append(PhrasalArticlePresenter.emphasize(word))
            elif not desired_word_indexes.isdisjoint({index - 2, index - 1, index + 1, index + 2}):
                snippet_words.append(word)
            else:
                if len(snippet_words) != 0:
                    snippets.append(' '.join(snippet_words))
                    snippet_words = []

        return snippets

    def process_contents(self, contents: str, consecutive_lemma_sets: Sequence[set[str]]) -> str:
        snippets = self.get_matching_snippets(contents, consecutive_lemma_sets)
        return ' ... '.join(snippets)

    def article_to_string(self, article: Article, consecutive_lemma_sets: Sequence[set[str]]) -> str:
        title = self.process_title(article.title, consecutive_lemma_sets)
        contents = self.process_contents(article.contents, consecutive_lemma_sets)
        return (f'{title}\n'
                f'{contents}')

    def present(self, articles: Iterable[Article], query: str):
        consecutive_lemma_sets = self.get_consecutive_lemma_sets(query)

        for article in articles:
            print(self.article_to_string(article, consecutive_lemma_sets))
            print()
