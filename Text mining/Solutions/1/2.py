from collections import defaultdict
from typing import AbstractSet, Collection, Callable
import unicodedata


def load_characters(path: str) -> AbstractSet[str]:
    with open(path, encoding='utf8') as file:
        return set('\n'.join(file.readlines()))


class Cluster:
    def __init__(self, name: str, contents: Collection[str]):
        self.name = name
        self.contents = contents

    def __str__(self) -> str:
        return f'{self.name} {" ".join(self.contents)}'


# According to https://pl.wikipedia.org/wiki/Alfabet_wietnamski, only Ơ, Ư are used only in vietnamese.
# Their codes are 416, 431. Between them, there are many letters from other alphabets.


def is_russian(character: str) -> bool:
    return ord('А') <= ord(character) <= ord('я')


def is_greek(character: str) -> bool:
    return ord('Α') <= ord(character) <= ord('Ω') or ord('α') <= ord(character) <= ord('ω')


def extract_letters(category_to_characters: defaultdict[str, list[str]],
                    predicate: Callable[[str], bool],
                    category_name: str):
    categories = set(category_to_characters.keys())

    for category in categories:
        desired_letters = list(filter(predicate, category_to_characters[category]))
        category_to_characters[category] = [character for character in category_to_characters[category]
                                            if character not in desired_letters]
        category_to_characters[category_name].extend(desired_letters)


# https://www.compart.com/en/unicode/category
category_names = {'Ll': 'Lowercase letters',
                  'Lo': 'Other letters',
                  'Mn': 'Nonspacing marks',
                  'Lu': 'Uppercase letters',
                  'Sm': 'Math symbols',
                  'No': 'Other numbers',
                  'Nd': 'Decimal numbers',
                  'Po': 'Other punctuation',
                  'Sk': 'Modifier symbols',
                  'Sc': 'Currency symbols',
                  'So': 'Other symbols',
                  'Nl': 'Number letters',
                  'Lm': 'Modifier letters',
                  'Mc': 'Spacing marks',
                  'Cf': 'Formatting',
                  'Pd': 'Dash punctuation',
                  'Pe': 'Close punctuation',
                  'Co': 'Private use',
                  'Cc': 'Control',
                  'Ps': 'Open punctuation',
                  'Zs': 'Space separators',
                  'Pf': 'Final punctuation',
                  'Lt': 'Titlecase letters',
                  'Me': 'Enclosing marks',
                  'Zl': 'Line separators',
                  'Pc': 'Connector punctuation',
                  'Zp': 'Paragraph separators',
                  'Cn': 'Non-characters',
                  'Pi': 'Initial punctuation'}


def get_category_name(category: str) -> str:
    return category_names.get(category, category)


def rename_categories(category_to_characters: dict[str, Collection[str]]):
    categories = set(category_to_characters.keys())

    for category in categories:
        cluster = category_to_characters[category]
        del category_to_characters[category]
        category_to_characters[get_category_name(category)] = cluster


def split_cluster(characters: list[str]) -> Collection[list[str]]:
    result = [[]]

    for i in range(len(characters) - 1):
        result[-1].append(characters[i])

        if ord(characters[i + 1]) - ord(characters[i]) >= 100:
            result.append([])

    result[-1].append(characters[-1])

    return result


def split_big_clusters(category_to_characters: defaultdict[str, list[str]]):
    categories = set(category_to_characters.keys())

    for category in categories:
        if 'letters' not in category:
            clusters = split_cluster(sorted(category_to_characters[category]))

            if len(clusters) > 1:
                del category_to_characters[category]

                for i, cluster in enumerate(clusters):
                    category_to_characters[f'{category}-{i}'] = cluster


# Categories to split (code difference): So (422), Mc (119), Sm (121), Mn (390), Nd (199)
# (Splitting if difference >= 100.)
def find_biggest_code_differences(category_to_characters: dict[str, Collection[str]]):
    for category in category_to_characters:
        cluster = sorted(category_to_characters[category])

        if len(cluster) >= 2:
            difference = max(range(len(cluster) - 1), key=lambda i: ord(cluster[i + 1]) - ord(cluster[i]))
            print(f'{category} {len(cluster)} {difference}')


def cluster_characters(characters: Collection[str]) -> Collection[Cluster]:
    category_to_characters = defaultdict(list)

    for character in characters:
        category_to_characters[unicodedata.category(character)].append(character)

    extract_letters(category_to_characters, is_russian, 'Russian alphabet')
    extract_letters(category_to_characters, is_greek, 'Greek alphabet')

    rename_categories(category_to_characters)

    split_big_clusters(category_to_characters)

    # find_biggest_code_differences(category_to_characters)

    return [Cluster(category, sorted(cluster))
            for category, cluster in category_to_characters.items()]


def clusters_to_string(clusters: Collection[Cluster]) -> str:
    return '\n'.join(str(cluster) for cluster in clusters)


def write_to_file(contents: str, path: str):
    with open(path, 'w', encoding='utf8') as file:
        file.write(contents)


def main():
    characters = load_characters('znaki_wikipedii.txt')
    clusters = cluster_characters(characters)
    write_to_file(clusters_to_string(clusters), '2 - clusters.txt')


if __name__ == '__main__':
    main()
