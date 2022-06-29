from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer, QuestionType
from search_engine.abstract_search_engine import AbstractSearchEngine
from tokenizer import Tokenizer
from utilities import scaled_edit_distance

from collections.abc import Container, Iterable, Sequence
from itertools import product
from typing import Optional


class GenericQuestionAnswerer(AbstractQuestionAnswerer):
    def __init__(self, search_engine: AbstractSearchEngine, tokenizer: Tokenizer):
        self.search_engine = search_engine
        self.tokenizer = tokenizer

    def search_for_titles(self, query: str) -> Iterable[str]:
        articles = self.search_engine.search(query)
        return [article.title for article in articles]

    def are_texts_similar(self, text_0: str, text_1: str) -> bool:
        tokens_0 = self.tokenizer.tokenize(text_0)
        tokens_1 = self.tokenizer.tokenize(text_1)

        for token_0, token_1 in product(tokens_0, tokens_1):
            if scaled_edit_distance(token_0.lower(), token_1.lower()) <= 0.5:
                return True

        return False

    @staticmethod
    def remove_parentheses_from_article_title(title: str) -> str:
        parenthesis_index = title.find('(')
        return (title if parenthesis_index == -1
                else title[:parenthesis_index])

    def search_answer_for_tokens(self, tokens: Iterable[str]) -> Optional[str]:
        query = ' '.join(tokens)
        article_titles = self.search_for_titles(query)

        for title in article_titles:
            if not self.are_texts_similar(query, title):
                return GenericQuestionAnswerer.remove_parentheses_from_article_title(title)

        return None

    def filter_tokens(self, tokens: Sequence[str]) -> Sequence[str]:
        # return tokens[1:]
        lowest_idf_token = min(tokens, key=lambda token: self.search_engine.idf(token))
        return tuple(token for token in tokens if token != lowest_idf_token)

    def answer(self, question: str) -> Optional[str]:
        tokens = self.tokenizer.tokenize(question)

        while len(tokens) > 0:
            found_answer = self.search_answer_for_tokens(tokens)

            if found_answer is None:
                tokens = self.filter_tokens(tokens)
            else:
                return found_answer

        return None

    def get_answered_question_types(self) -> Container[QuestionType]:
        return QuestionType.GENERIC,
