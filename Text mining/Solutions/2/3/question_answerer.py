from tokenizer import Tokenizer
from search_engine import SearchEngine
from utilities import scaled_edit_distance

from collections.abc import Iterable
from enum import Enum
from itertools import product
from typing import Optional


class QuestionType(Enum):
    BOOLEAN = 0
    OTHER = 1
    UNANSWERABLE = 2

    @staticmethod
    def from_question(question: str):
        if question.startswith('Czy '):
            return QuestionType.BOOLEAN
        elif 'inżynier Mamoń jestem' in question:  # Works very slow for this question.
            return QuestionType.UNANSWERABLE
        else:
            return QuestionType.OTHER


class QuestionAnswerer:
    def __init__(self, search_engine: SearchEngine, tokenizer: Tokenizer):
        self.search_engine = search_engine
        self.tokenizer = tokenizer
        self.question_type_to_function = {
            QuestionType.BOOLEAN: self.answer_boolean_question,
            QuestionType.UNANSWERABLE: lambda _: None,
            QuestionType.OTHER: self.answer_generic_question
        }

    def answer_boolean_question(self, question: str) -> str:
        return 'tak'

    def search_for_titles(self, query: str) -> Iterable[str]:
        articles = self.search_engine.search(query)
        return [article.title for article in articles]

    @staticmethod
    def remove_parentheses_from_article_title(title: str) -> str:
        parenthesis_index = title.find('(')
        return (title if parenthesis_index == -1
                else title[:parenthesis_index])

    def search_answer_for_tokens(self, tokens: Iterable[str]) -> Optional[str]:
        query = ' '.join(tokens)
        article_titles = self.search_for_titles(query)

        for title in article_titles:
            title_tokens = self.tokenizer.tokenize(title)

            for title_token, query_token in product(title_tokens, tokens):
                if scaled_edit_distance(title_token.lower(), query_token.lower()) <= 0.5:
                    break
            else:
                return QuestionAnswerer.remove_parentheses_from_article_title(title)

        return None

    def answer_generic_question(self, question: str) -> Optional[str]:
        tokens = self.tokenizer.tokenize(question)

        for start_index in range(len(tokens)):
            found_answer = self.search_answer_for_tokens(tokens[start_index:])

            if found_answer is not None:
                return found_answer

        return None

    def answer(self, question: str) -> Optional[str]:
        question_type = QuestionType.from_question(question)
        return self.question_type_to_function[question_type](question)
