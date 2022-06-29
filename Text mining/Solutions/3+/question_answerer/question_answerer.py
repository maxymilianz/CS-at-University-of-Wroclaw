from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer, QuestionType

from collections.abc import Collection, Container
from typing import Optional


class QuestionAnswerer(AbstractQuestionAnswerer):
    def __init__(self,
                 generic_question_answerer: AbstractQuestionAnswerer,
                 specialized_answerers: Collection[AbstractQuestionAnswerer]):
        self.generic_question_answerer = generic_question_answerer
        self.specialized_answerers = specialized_answerers

    def answer(self, question: str) -> Optional[str]:
        question_type = QuestionType.from_question(question)

        for answerer in self.specialized_answerers:
            if question_type in answerer.get_answered_question_types():
                return answerer.answer(question)

        return self.generic_question_answerer.answer(question)

    def get_answered_question_types(self) -> Container[QuestionType]:
        return tuple(QuestionType)
