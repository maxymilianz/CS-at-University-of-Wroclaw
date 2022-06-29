from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer, QuestionType
from search_engine.abstract_search_engine import AbstractSearchEngine
from tokenizer import Tokenizer
from wikipedia_io import Article

from collections.abc import Container, Sequence
from math import ceil
import re
from typing import Optional


class YearQuestionAnswerer(AbstractQuestionAnswerer):
    def __init__(self, tokenizer: Tokenizer, search_engine: AbstractSearchEngine):
        self.tokenizer = tokenizer
        self.search_engine = search_engine

    @staticmethod
    def extract_year_from_article(article: Article) -> Optional[str]:
        match = re.search(r'\d{4}', article.contents)
        return (None if match is None
                else match.group(0))

    def search_for_answer_for_query(self, query: str) -> Optional[str]:
        articles = tuple(self.search_engine.search(query))
        return (None if len(articles) == 0
                else YearQuestionAnswerer.extract_year_from_article(articles[0]))

    def filter_tokens(self, tokens: Sequence[str]) -> Sequence[str]:
        lowest_idf_token = min(tokens, key=lambda token: self.search_engine.idf(token))
        return tuple(token for token in tokens if token != lowest_idf_token)

    def search_for_answer(self, question: str) -> Optional[str]:
        tokens = self.tokenizer.tokenize(question)

        while len(tokens) > 0:
            query = ' '.join(tokens)
            found_answer = self.search_for_answer_for_query(query)

            if found_answer is None:
                tokens = self.filter_tokens(tokens)
            else:
                return found_answer

        return None

    @staticmethod
    def year_to_century(year: str) -> str:
        number = int(year)
        return str(ceil(number / 100))

    @staticmethod
    def format_answer(question: str, answer: str) -> str:
        is_year_question = question.startswith('W którym roku')
        return (answer if is_year_question
                else YearQuestionAnswerer.year_to_century(answer))

    def answer(self, question: str) -> Optional[str]:
        answer = self.search_for_answer(question)
        return (None if answer is None
                else YearQuestionAnswerer.format_answer(question, answer))

    def get_answered_question_types(self) -> Container[QuestionType]:
        return QuestionType.CENTURY, QuestionType.YEAR
