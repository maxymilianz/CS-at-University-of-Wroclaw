from index_manager.abstract_index_manager import IndexManager
from index_manager.file_index_manager import FileIndexManager
from lemmatizer import Lemmatizer, MorfologikLemmatizer
from position_to_article_mapper import FilePositionToArticleMapper, PositionToArticleMapper
from wikipedia_io import Article, WikipediaFileIo

from typing import Iterable


class PositionalIndexCreator:
    def __init__(self,
                 lemmatizer: Lemmatizer,
                 index_manager: IndexManager,
                 position_to_article_mapper: PositionToArticleMapper):
        self.lemmatizer = lemmatizer
        self.index_manager = index_manager
        self.position_to_article_mapper = position_to_article_mapper
        self.position = 0

    def process_word(self, word: str):
        lemmas = self.lemmatizer.lemmatize(word)

        for lemma in lemmas:
            self.index_manager.add_to_index(lemma, self.position)

    def process_article(self, article: Article):
        text = str(article)

        for word in text.split():
            if word.isalpha():
                self.process_word(word)
            self.position += 1  # incremented also if "word" is e.g. punctuation

    def create_index(self, articles: Iterable[Article]):
        for article in articles:
            if article.id % 10000 == 0:
                print(f'Processing article {article.id}.')

            self.position_to_article_mapper.set_first_position_for_article(article.id, self.position)
            self.process_article(article)
            self.position += 1  # between articles

        self.index_manager.save_index()


def main():
    wikipedia_io = WikipediaFileIo('resources/small_wikipedia.txt')
    lemmatizer = MorfologikLemmatizer('resources/polimorfologik-2.1.txt')
    index_manager = FileIndexManager('resources/positional_index.txt', 'resources/positional_index_offsets.txt')
    position_to_article_mapper = FilePositionToArticleMapper('resources/first_positions.txt')
    index_creator = PositionalIndexCreator(lemmatizer, index_manager, position_to_article_mapper)
    index_creator.create_index(wikipedia_io.get_all_articles())


if __name__ == '__main__':
    main()
