from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer, QuestionType

from collections.abc import Container


class AffirmativeQuestionAnswerer(AbstractQuestionAnswerer):
    def answer(self, question: str) -> str:
        return 'tak'

    def get_answered_question_types(self) -> Container[QuestionType]:
        return QuestionType.BOOLEAN,
