from index_manager.abstract_index_manager import IndexManager

from collections import defaultdict
from functools import reduce
from operator import or_
import os
from typing import Collection, Iterable


class FileIndexManager(IndexManager):
    def __init__(self, index_path: str, offsets_path: str):
        self.index_path = index_path
        self.offsets_path = offsets_path
        self.index = defaultdict(list)
        self.offsets = self.get_offsets()

    @staticmethod
    def parse_word_and_offset(line: str) -> tuple[str, int]:
        words = line.split()
        return ' '.join(words[:-1]), int(words[-1])

    def load_offsets(self) -> dict[str, int]:
        with open(self.offsets_path, encoding='utf8') as file:
            return {word: offset for word, offset
                    in map(FileIndexManager.parse_word_and_offset, file.readlines())}

    def get_offsets(self) -> dict[str, int]:
        if os.path.isfile(self.offsets_path):
            return self.load_offsets()
        else:
            return {}

    def add_to_index(self, word: str, document_id: int):
        self.index[word].append(document_id)

    def save_word_and_document_ids(self, word: str, document_ids: Iterable[str]):
        with open(self.index_path, 'a+', encoding='utf8') as file:
            file.write(f'{word}: {" ".join(map(str, document_ids))}\n')

    def get_current_offset(self) -> int:
        return os.path.getsize(self.index_path)

    def offsets_to_string(self) -> str:
        return '\n'.join(f'{word} {offset}'
                         for word, offset in sorted(self.offsets.items()))

    def save_offsets(self):
        with open(self.offsets_path, 'w', encoding='utf8') as file:
            file.write(self.offsets_to_string())

    def save_index(self):
        offset = 0

        for word, document_ids in sorted(self.index.items()):
            self.save_word_and_document_ids(word, document_ids)
            self.offsets[word] = offset
            offset = self.get_current_offset()

        self.save_offsets()

    @staticmethod
    def parse_posting_list(line: str) -> set[int]:
        article_ids = line.split(':')[1].split()
        return set(map(int, article_ids))

    def load_posting_list(self, offset: int) -> set[int]:
        with open(self.index_path, encoding='utf8') as file:
            file.seek(offset)
            return FileIndexManager.parse_posting_list(file.readline())

    def get_posting_list_for_word(self, word: str) -> set[int]:
        if word in self.offsets:
            return self.load_posting_list(self.offsets[word])
        else:
            return set()

    def get_posting_list(self, words: Collection[str]) -> set[int]:
        return reduce(or_, map(self.get_posting_list_for_word, words), set())
