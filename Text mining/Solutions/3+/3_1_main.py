from default_object_factories import get_article_presenter, get_search_engine


def main():
    phrasal_search_engine = get_search_engine(phrasal=True)
    phrasal_article_presenter = get_article_presenter(phrasal=True)

    while True:
        query = input('What are you looking for?')
        results = phrasal_search_engine.search(query)
        phrasal_article_presenter.present(results, query)


if __name__ == '__main__':
    main()
