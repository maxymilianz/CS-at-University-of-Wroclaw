from typing import Collection


class IndexManager:
    def add_to_index(self, word: str, document_id: int):
        raise NotImplementedError

    def save_index(self):
        raise NotImplementedError

    def get_posting_list(self, words: Collection[str]) -> set[int]:
        raise NotImplementedError
