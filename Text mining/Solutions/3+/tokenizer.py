from utilities import extract_words

from collections.abc import Sequence
import spacy


class Tokenizer:
    def tokenize(self, text: str) -> Sequence[str]:
        raise NotImplementedError


class ExtractWordsTokenizer(Tokenizer):
    def tokenize(self, text: str) -> Sequence[str]:
        return extract_words(text)


class SpacyTokenizer(Tokenizer):
    def __init__(self, spacy_name: str):
        self.spacy_model = spacy.load(spacy_name)

    def tokenize(self, text: str) -> Sequence[str]:
        return tuple(map(str, self.spacy_model(text)))
