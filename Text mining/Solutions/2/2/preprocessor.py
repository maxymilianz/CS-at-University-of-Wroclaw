from index_manager import FileIndexManager
from lemmatizer import Lemmatizer, MorfologikLemmatizer
from wikipedia_io import WikipediaFileIo, WikipediaIo


class Preprocessor:
    def __init__(self,
                 target_wikipedia_io: WikipediaIo,
                 lemmatizer: Lemmatizer,
                 index_manager: FileIndexManager):
        self.target_wikipedia_io = target_wikipedia_io
        self.lemmatizer = lemmatizer
        self.index_manager = index_manager

    def update_index(self, article: str, article_id: int):
        for lemma in self.lemmatizer.get_lemmas_for_text(article):
            self.index_manager.add_to_index(lemma, article_id)

    def process_article(self, article: str):
        self.target_wikipedia_io.add_article(article)
        article_id = self.target_wikipedia_io.get_last_article_id()
        self.update_index(article, article_id)

    @staticmethod
    def is_title_line(line: str) -> bool:
        return line.startswith('TITLE: ')

    def preprocess(self, source_wikipedia_path: str):
        with open(source_wikipedia_path, encoding='utf8') as source_wikipedia_file:
            wikipedia_lines = source_wikipedia_file.readlines()
            line_count = len(wikipedia_lines)
            article = ''

            for line_number, line in enumerate(wikipedia_lines):
                if line_number % 100000 == 0:
                    print(f'{line_number} / {line_count} lines processed')

                if line.isspace():
                    self.process_article(article)
                    article = ''
                elif Preprocessor.is_title_line(line):
                    pass  # Title is repeated in the next line.
                else:
                    article += line

        self.target_wikipedia_io.save_wikipedia()
        self.index_manager.save_index()


def main():
    target_wikipedia_io = WikipediaFileIo('small_wikipedia.txt')
    lemmatizer = MorfologikLemmatizer('../polimorfologik-2.1.txt')
    index_manager = FileIndexManager('index.txt', 'offsets.txt')

    preprocessor = Preprocessor(target_wikipedia_io, lemmatizer, index_manager)
    preprocessor.preprocess('fp_wiki.txt')


if __name__ == '__main__':
    main()
