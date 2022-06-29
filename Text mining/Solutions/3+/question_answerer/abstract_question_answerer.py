from enum import Enum
from typing import Container, Optional


class QuestionType(Enum):
    GENERIC = 0
    UNANSWERABLE = 1

    BOOLEAN = 2
    YEAR = 3
    CENTURY = 4
    HUMAN_NAME = 5
    NAME = 6
    ADAGE = 7

    @staticmethod
    def from_question(question: str):
        if question.startswith('Czy '):
            return QuestionType.BOOLEAN
        elif question.startswith('W którym roku'):
            return QuestionType.YEAR
        elif question.startswith('W którym wieku'):
            return QuestionType.CENTURY
        elif question.startswith('Kto '):
            return QuestionType.HUMAN_NAME
        elif question.startswith('Jak nazywa'):
            return QuestionType.NAME
        elif 'przysłowi' in question:
            return QuestionType.ADAGE
        elif 'inżynier Mamoń' in question:  # Works very slow for this question.
            return QuestionType.UNANSWERABLE
        else:
            return QuestionType.GENERIC


class AbstractQuestionAnswerer:
    def answer(self, question: str) -> Optional[str]:
        raise NotImplementedError

    def get_answered_question_types(self) -> Container[QuestionType]:
        raise NotImplementedError
