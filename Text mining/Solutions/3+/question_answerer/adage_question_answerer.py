from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer, QuestionType
from utilities import extract_words

from collections.abc import Collection, Container
from typing import Optional


class AdageQuestionAnswerer(AbstractQuestionAnswerer):
    def __init__(self, adages: Collection[str]):
        self.adages = adages

    def similarity(self, adage: str, question: str) -> float:
        adage_words = extract_words(adage)
        question_words = extract_words(question)
        return len(list(filter(lambda word: word in adage_words, question_words)))

    def get_adage_for_question(self, question: str) -> str:
        return max(self.adages, key=lambda adage: self.similarity(adage, question))

    def extract_missing_part(self, adage: str, question: str) -> str:
        adage_words = extract_words(adage)
        question_words = extract_words(question)
        potential_results = []
        result_words = []

        for word in adage_words:
            if word in question_words:
                if len(result_words) != 0:
                    potential_results.append(result_words)
                    result_words = []
            else:  # word not in question
                result_words.append(word)

        potential_results.append(result_words)

        return ' '.join(max(potential_results, key=len))

    def answer(self, question: str) -> Optional[str]:
        adage = self.get_adage_for_question(question)
        answer = self.extract_missing_part(adage, question)
        return answer

    def get_answered_question_types(self) -> Container[QuestionType]:
        return QuestionType.ADAGE,
