from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer, QuestionType
from similar_definition_finder.similar_definition_finder import SimilarDefinitionFinder

from collections.abc import Container
from typing import Optional


class NameQuestionAnswerer(AbstractQuestionAnswerer):
    def __init__(self, similar_definition_finder: SimilarDefinitionFinder):
        self.similar_definition_finder = similar_definition_finder

    @staticmethod
    def extract_description_from_question(question: str) -> str:
        return ' '.join(question.split()[3:])

    def answer(self, question: str) -> Optional[str]:
        description = NameQuestionAnswerer.extract_description_from_question(question)
        similar_definitions = self.similar_definition_finder.get_similar_definitions(description)

        if len(similar_definitions) != 0:
            print(similar_definitions[0].name)

        return (None if len(similar_definitions) == 0
                else similar_definitions[0].name)

    def get_answered_question_types(self) -> Container[QuestionType]:
        return QuestionType.NAME,
