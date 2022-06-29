from default_object_factories import get_morfologik_lemmatizer, get_wikipedia_file_io
from index_manager.abstract_index_manager import IndexManager
from index_manager.file_index_manager import FileIndexManager
from lemmatizer import Lemmatizer
from wikipedia_io import Article

from collections.abc import Iterable


class TitleIndexCreator:
    def __init__(self, lemmatizer: Lemmatizer, index_manager: IndexManager):
        self.lemmatizer = lemmatizer
        self.index_manager = index_manager

    def process_article(self, article: Article):
        for lemma in self.lemmatizer.get_lemmas_for_text(article.title):
            self.index_manager.add_to_index(lemma, article.id)

    def create(self, articles: Iterable[Article]):
        for article in articles:
            if article.id % 100000 == 0:
                print(f'Creating title index for article {article.id}.')

            self.process_article(article)

        self.index_manager.save_index()


def main():
    lemmatizer = get_morfologik_lemmatizer()
    index_manager = FileIndexManager('resources/title_index.txt', 'resources/title_index_offsets.txt')
    title_index_creator = TitleIndexCreator(lemmatizer, index_manager)
    wikipedia_io = get_wikipedia_file_io()

    title_index_creator.create(wikipedia_io.get_all_articles())


if __name__ == '__main__':
    main()
