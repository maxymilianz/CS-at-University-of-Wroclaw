from collections import defaultdict
import os
from typing import Iterable


class PostingList:
    def __init__(self, document_ids: Iterable[int] = ()):
        self.document_ids = set(document_ids)

    def __and__(self, other):
        return PostingList(self.document_ids.intersection(other.document_ids))


class IndexManager:
    def add_to_index(self, word: str, document_id: int):
        raise NotImplementedError

    def save_index(self):
        raise NotImplementedError

    def get_posting_list(self, word: str) -> PostingList:
        raise NotImplementedError


class FileIndexManager(IndexManager):
    def __init__(self, index_path: str, offsets_path: str):
        self.index_path = index_path
        self.offsets_path = offsets_path
        self.word_to_document_ids = defaultdict(list)
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
        self.word_to_document_ids[word].append(document_id)

    def save_word_and_document_ids(self, word: str, document_ids: Iterable[str]):
        with open(self.index_path, 'a+', encoding='utf8') as file:
            file.write(f'{word}: {" ".join(map(str, document_ids))}\n')

    def get_current_offset(self) -> int:
        return os.path.getsize(self.index_path)

    def offsets_to_string(self) -> str:
        return '\n'.join(f'{word} {offset}'
                         for word, offset in sorted(self.offsets.items()))

    def save_word_to_offset(self):
        with open(self.offsets_path, 'w', encoding='utf8') as file:
            file.write(self.offsets_to_string())

    def save_index(self):
        offset = 0

        for word, document_ids in sorted(self.word_to_document_ids.items()):
            self.save_word_and_document_ids(word, document_ids)
            self.offsets[word] = offset
            offset = self.get_current_offset()

        self.save_word_to_offset()

    @staticmethod
    def parse_posting_list(line: str) -> PostingList:
        article_ids = line.split(':')[1].split()
        return PostingList(map(int, article_ids))

    def load_posting_list(self, offset: int) -> PostingList:
        with open(self.index_path, encoding='utf8') as file:
            file.seek(offset)
            return FileIndexManager.parse_posting_list(file.readline())

    def get_posting_list(self, word: str) -> PostingList:
        if word in self.offsets:
            return self.load_posting_list(self.offsets[word])
        else:
            return PostingList()
