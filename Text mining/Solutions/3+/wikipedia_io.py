import os
from typing import Iterable, Optional, Sequence, TextIO


class Article:
    def __init__(self, id: int, title: str, contents: str):
        self.id = id
        self.title = title
        self.contents = contents

    def __str__(self):
        return f'{self.title}:\n{self.contents}'

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __hash__(self):
        return self.id


class WikipediaIo:
    def add_article(self, article: str):
        raise NotImplementedError

    def get_last_article_id(self) -> int:
        raise NotImplementedError

    def save_wikipedia(self):
        raise NotImplementedError

    def find_article(self, article_id: int) -> Article:
        raise NotImplementedError

    def get_all_articles(self) -> Iterable[Article]:
        raise NotImplementedError


class NotTitleLineException(Exception):
    pass


class WikipediaFileIo(WikipediaIo):
    def __init__(self, wikipedia_path: str):
        self.wikipedia_path = wikipedia_path
        self.article_count = self.get_article_count()
        # ^ kept here, because this class is responsible for binary-searching and maintaining the id order.
        self.article_strings = []

    def load_article_count(self) -> int:
        with open(self.wikipedia_path, encoding='utf8') as file:
            return int(file.readline())

    def get_article_count(self) -> int:
        if os.path.isfile(self.wikipedia_path):
            return self.load_article_count()
        else:
            return 0

    def add_article(self, article: str):
        self.article_strings.append(f'{self.article_count} {article}')
        self.article_count += 1

    def get_last_article_id(self) -> int:
        return self.article_count - 1

    def articles_to_string(self) -> str:
        return '\n'.join(self.article_strings)

    def save_wikipedia(self):
        with open(self.wikipedia_path, 'a+', encoding='utf8') as file:
            file.write(f'{self.article_count}\n\n{self.articles_to_string()}')

    @staticmethod
    def skip_up_to_next_empty_line(file: TextIO, offset: int):
        file.seek(offset)

        try:
            file.readline()
            # ^ may return '\n' if the cursor is just before '\n' in a nonempty line.
            line = file.readline()
            while not line.isspace():
                line = file.readline()
        except UnicodeDecodeError:
            WikipediaFileIo.skip_up_to_next_empty_line(file, offset + 1)

    @staticmethod
    def get_article_id_from_title_line(line: str) -> int:
        words = line.split()

        try:
            return int(words[0])
        except (IndexError, ValueError):
            raise NotTitleLineException

    @staticmethod
    def get_nearest_article_id(file: TextIO, offset: int) -> Optional[int]:
        WikipediaFileIo.skip_up_to_next_empty_line(file, offset)
        potential_title_line = file.readline()

        try:
            return WikipediaFileIo.get_article_id_from_title_line(potential_title_line)
        except NotTitleLineException:
            return None

    @staticmethod
    def read_to_next_empty_line(file: TextIO) -> Sequence[str]:
        lines = []

        line = file.readline()
        while not (line.isspace() or line == ''):
            lines.append(line)
            line = file.readline()

        return lines

    @staticmethod
    def parse_article_id_and_title(title_line: str) -> tuple[int, str]:
        words = title_line.split()
        id = int(words[0])
        title = ' '.join(words[1:])
        return id, title

    @staticmethod
    def parse_article(lines: Sequence[str]) -> Article:
        title_line = lines[0]
        id, title = WikipediaFileIo.parse_article_id_and_title(title_line)
        contents = ''.join(lines[1:])
        return Article(id, title, contents)

    @staticmethod
    def get_nearest_article(file: TextIO, offset: int) -> Article:
        WikipediaFileIo.skip_up_to_next_empty_line(file, offset)
        lines = WikipediaFileIo.read_to_next_empty_line(file)
        return WikipediaFileIo.parse_article(lines)

    def find_article(self, article_id: int) -> Article:
        file_size = os.path.getsize(self.wikipedia_path)

        a = 0
        b = file_size - 1

        with open(self.wikipedia_path, encoding='utf8') as file:
            while a < b:
                mid = (a + b) // 2
                middle_value = WikipediaFileIo.get_nearest_article_id(file, offset=mid)

                if middle_value is None or article_id < middle_value:  # None - mid is after start of the last article.
                    b = mid
                elif article_id == middle_value:
                    return WikipediaFileIo.get_nearest_article(file, offset=mid)
                else:  # desired_value > middle_value
                    a = mid

        raise Exception(f'Binary search for article {article_id} has failed.')

    def get_all_articles(self) -> Iterable[Article]:
        articles = []

        with open(self.wikipedia_path, encoding='utf8') as file:
            file.readline()
            file.readline()
            # ^ skip article count

            lines = WikipediaFileIo.read_to_next_empty_line(file)

            while len(lines) > 0:
                article = WikipediaFileIo.parse_article(lines)
                articles.append(article)
                lines = WikipediaFileIo.read_to_next_empty_line(file)

        return articles
