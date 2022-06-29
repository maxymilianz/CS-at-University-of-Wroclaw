from default_object_factories import get_article_presenter, get_corrector, get_one_title_search_engine, WordSource

from time import time


def main():
    corrector = get_corrector(WordSource.SMALL_WIKIPEDIA)
    one_title_search_engine = get_one_title_search_engine()
    article_presenter = get_article_presenter(phrasal=False)

    while True:
        query = input('What are you looking for?')

        correct_start_time = time()
        correct_query = corrector.correct(query)
        print(f'Corrected in {time() - correct_start_time} s.')

        print(f'Looking for "{correct_query}".')

        results = one_title_search_engine.search(correct_query)
        article_presenter.present(results, correct_query)


if __name__ == '__main__':
    main()
