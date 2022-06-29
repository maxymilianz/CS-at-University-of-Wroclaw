import re
from typing import Collection
import unicodedata


class NoMoreSnippet(Exception):
    pass


class ArticleSnippet:
    def __init__(self, title: str, contents: str):
        self.title = title
        self.contents = contents

    def __str__(self) -> str:
        return f'{self.title}: {self.contents}'

    @staticmethod
    def title_from_stream(stream) -> str:
        line = stream.readline()
        try_count = 1

        while not line.startswith('###'):
            if try_count < 10:
                line = stream.readline()
                try_count += 1
            else:
                raise NoMoreSnippet

        return line[3:].strip()

    @staticmethod
    def contents_from_stream(stream) -> str:
        return stream.readline()

    @staticmethod
    def from_stream(stream):
        try:
            title = ArticleSnippet.title_from_stream(stream)
            contents = ArticleSnippet.contents_from_stream(stream)
            return ArticleSnippet(title, contents)
        except NoMoreSnippet:
            return None


def load_article_snippets(path: str) -> Collection[ArticleSnippet]:
    result = []

    with open(path, encoding="utf8") as data:
        snippet = ArticleSnippet.from_stream(data)

        while snippet is not None:
            result.append(snippet)
            snippet = ArticleSnippet.from_stream(data)

    return result


def is_latin(character: str) -> bool:
    return 'LATIN' in unicodedata.name(character)


def is_polish(text: str) -> bool:
    return all(is_latin(character) for character in text if character.isalpha())


def is_good_synonym(word: str, synonyms: Collection[str]) -> bool:
    return (all(synonym.lower() != word.lower() for synonym in synonyms) and
            all(not synonym.startswith(word) for synonym in synonyms) and
            len(word) > 1 and
            is_polish(word))


def find_synonyms_in_snippet(snippet: ArticleSnippet) -> Collection[str]:
    result = {snippet.title}
    regex_matches = re.findall("'''.*?'''", snippet.contents)

    for word in [word.strip("'").strip() for word in regex_matches]:
        if is_good_synonym(word, result):
            result.add(word)

    return result


def find_synonyms(article_snippets: Collection[ArticleSnippet]) -> Collection[Collection[str]]:
    return [words for words in [find_synonyms_in_snippet(snippet) for snippet in article_snippets] if len(words) > 1]


def synonyms_to_string(synonyms: Collection[Collection[str]]) -> str:
    return '\n'.join(' # '.join(words) for words in synonyms)


def write_to_file(contents: str, path: str):
    with open(path, 'w', encoding='utf8') as file:
        file.write(contents)


def main():
    article_snippets = load_article_snippets('poczatki_wikipediowe.txt')
    synonyms = find_synonyms(article_snippets)
    write_to_file(synonyms_to_string(synonyms), '1 - new.txt')


if __name__ == '__main__':
    main()
