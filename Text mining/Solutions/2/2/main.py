from article_presenter import ArticlePresenter
from index_manager import FileIndexManager
from lemmatizer import MorfologikLemmatizer
from search_engine import MatchRating, SearchEngine
from wikipedia_io import WikipediaFileIo


def main():
    lemmatizer = MorfologikLemmatizer('../polimorfologik-2.1.txt')
    index_manager = FileIndexManager('index.txt', 'offsets.txt')
    wikipedia_io = WikipediaFileIo('small_wikipedia.txt')
    match_rating = MatchRating(wikipedia_io.get_last_article_id(), lemmatizer)

    search_engine = SearchEngine(lemmatizer, index_manager, wikipedia_io, match_rating)
    article_presenter = ArticlePresenter(lemmatizer)

    while True:
        query = input('What are you looking for?')
        results = search_engine.search(query)
        article_presenter.present(results, query)


if __name__ == '__main__':
    main()
