from index_manager import FileIndexManager
from tokenizer import ExtractWordsTokenizer, SpacyTokenizer
from lemmatizer import MorfologikLemmatizer
from question_answerer import QuestionAnswerer
from search_engine import MatchRating, SearchEngine
from wikipedia_io import WikipediaFileIo

from collections.abc import Iterable
from typing import Optional


def load_questions(path: str) -> Iterable[str]:
    with open(path, encoding='utf8') as file:
        return file.readlines()


def answer_questions(question_answerer: QuestionAnswerer, questions: Iterable[str]) -> Iterable[str]:
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
    lemmatizer = MorfologikLemmatizer('../polimorfologik-2.1.txt')
    index_manager = FileIndexManager('../2/index.txt', '../2/offsets.txt')
    wikipedia_io = WikipediaFileIo('../2/small_wikipedia.txt')
    match_rating = MatchRating(wikipedia_io.get_last_article_id(), lemmatizer)
    search_engine = SearchEngine(lemmatizer, index_manager, wikipedia_io, match_rating)

    # tokenizer = SpacyTokenizer("pl_core_news_sm")
    tokenizer = ExtractWordsTokenizer()

    question_answerer = QuestionAnswerer(search_engine, tokenizer)

    questions = load_questions('pytania.txt')
    answers = answer_questions(question_answerer, questions)
    save_answers_to_file(answers, 'answers.txt')


if __name__ == '__main__':
    main()
