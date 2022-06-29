from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer, QuestionType
from search_engine.abstract_search_engine import AbstractSearchEngine
from tokenizer import Tokenizer
from utilities import scaled_edit_distance
from wikipedia_io import Article

from itertools import product
from typing import Container, Optional, Sequence


class HumanNameQuestionAnswerer(AbstractQuestionAnswerer):
    def __init__(self, tokenizer: Tokenizer, search_engine: AbstractSearchEngine):
        self.tokenizer = tokenizer
        self.search_engine = search_engine

    def are_texts_similar(self, text_0: str, text_1: str) -> bool:
        tokens_0 = self.tokenizer.tokenize(text_0)
        tokens_1 = self.tokenizer.tokenize(text_1)

        for token_0, token_1 in product(tokens_0, tokens_1):
            if scaled_edit_distance(token_0.lower(), token_1.lower()) <= 0.5:
                return True

        return False

    def extract_name_from_article(self, article: Article, query: str) -> Optional[str]:
        name_words = []

        for word in self.tokenizer.tokenize(article.contents):
            if word[0].isupper():
                name_words.append(word)
            else:
                name = ' '.join(name_words)

                if self.are_texts_similar(query, name):
                    name_words.clear()
                else:
                    return name

        return None

    def search_for_answer_for_query(self, query: str) -> Optional[str]:
        articles = tuple(self.search_engine.search(query))
        return (None if len(articles) == 0
                else self.extract_name_from_article(articles[0], query))

    def filter_tokens(self, tokens: Sequence[str]) -> Sequence[str]:
        lowest_idf_token = min(tokens, key=lambda token: self.search_engine.idf(token))
        return tuple(token for token in tokens if token != lowest_idf_token)

    def answer(self, question: str) -> Optional[str]:
        tokens = self.tokenizer.tokenize(question)

        while len(tokens) > 0:
            query = ' '.join(tokens)
            found_answer = self.search_for_answer_for_query(query)

            if found_answer is None:
                tokens = self.filter_tokens(tokens)
            else:
                return found_answer

        return None

    def get_answered_question_types(self) -> Container[QuestionType]:
        return QuestionType.HUMAN_NAME,
