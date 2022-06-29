from default_object_factories import DefinitionSource, get_question_answerer
from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer

from collections.abc import Iterable
from typing import Optional


def load_questions(path: str) -> Iterable[str]:
    with open(path, encoding='utf8') as file:
        return file.readlines()


def answer_questions(question_answerer: AbstractQuestionAnswerer, questions: Iterable[str]) -> Iterable[str]:
    answers = []

    for question_number, question in enumerate(questions):
        if question_number % 10 == 0:
            print(f'Question #{question_number}')

        answers.append(question_answerer.answer(question))

    return map(str, answers)


def save_answers_to_file(answers: Iterable[Optional[str]], path: str):
    with open(path, 'w', encoding='utf8') as file:
        file.write('\n'.join(answers))


def main():
    question_answerer = get_question_answerer(phrasal=False, definition_source=DefinitionSource.WIKTIONARY)

    questions = load_questions('resources/pytania.txt')
    answers = answer_questions(question_answerer, questions)
    save_answers_to_file(answers, 'resources/answers.txt')


if __name__ == '__main__':
    main()
