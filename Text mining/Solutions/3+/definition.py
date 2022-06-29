from wikipedia_io import Article

from collections.abc import Collection, Iterable


class Definition:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


def parse_wiktionary_definition(line: str) -> Definition:
    name, description = line.split(' ### ')
    return Definition(name, description)


def load_definitions_from_wiktionary(path: str) -> Collection[Definition]:
    with open(path, encoding='utf8') as file:
        return set(map(parse_wiktionary_definition, file.readlines()))


def article_to_definition(article: Article) -> Definition:
    description = article.contents.split('. ')[0]
    return Definition(article.title, description)


def load_definitions_from_articles(articles: Iterable[Article]) -> Collection[Definition]:
    return set(map(article_to_definition, articles))
