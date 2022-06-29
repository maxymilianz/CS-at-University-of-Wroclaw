from lemmatizer import Lemmatizer
from utilities import extract_words, unzip

from collections import defaultdict
from random import choices
from typing import Iterable, Mapping


class Interlocutor:
    def reply(self, line: str) -> str:
        raise NotImplementedError


class InputInterlocutor(Interlocutor):
    def reply(self, line: str) -> str:
        print(line)
        return input()


class MasterOfPunchyRetort(Interlocutor):
    def __init__(self, quotes: Iterable[str], lemmatizer: Lemmatizer, should_randomize_reply: bool):
        self.quotes = quotes
        self.used_quotes = set()

        self.lemmatizer = lemmatizer
        self.quote_to_lemmas = self.create_quote_to_lemmas()
        self.lemma_counts = self.get_lemma_counts()

        self.should_randomize_reply = should_randomize_reply
        self.input_line = None

    def create_quote_to_lemmas(self) -> Mapping[str, set[str]]:
        return {quote: self.lemmatizer.get_lemmas_for_text(quote) for quote in self.quotes}

    def get_lemma_counts(self) -> Mapping[str, int]:
        lemma_counts = defaultdict(lambda: 0)

        for lemmas in self.quote_to_lemmas.values():
            for lemma in lemmas:
                lemma_counts[lemma] += 1

        return lemma_counts

    def rate_quote_suitability(self, quote: str, lemmas: set[str]) -> float:
        lemmas_intersection = self.quote_to_lemmas[quote].intersection(lemmas)
        return sum(1 / self.lemma_counts[lemma] for lemma in lemmas_intersection)

    def get_quote_ranking(self) -> Iterable[tuple[str, float]]:
        lemmas = self.lemmatizer.get_lemmas_for_text(self.input_line)
        ranking = ((quote, self.rate_quote_suitability(quote, lemmas))
                   for quote in self.quotes)
        return sorted(ranking,
                      key=lambda quote_and_score: quote_and_score[1],
                      reverse=True)[:100]

    @staticmethod
    def are_texts_similar(text_0: str, text_1: str) -> bool:
        words_0 = set(extract_words(text_0))
        words_1 = set(extract_words(text_1))
        return len(words_0.symmetric_difference(words_1)) <= 1

    @staticmethod
    def is_quote_generic(quote: str) -> bool:
        return any(word in quote for word in ['on', 'go', 'ona', 'ją', 'ono', 'oni', 'ich', 'one', 'je'])

    def process_score(self, quote: str, score: float) -> float:
        if MasterOfPunchyRetort.are_texts_similar(quote, self.input_line):
            return -1
        else:
            if quote in self.used_quotes:
                score *= 0.25
            if MasterOfPunchyRetort.is_quote_generic(quote):
                score *= 0.5
            return score

    @staticmethod
    def randomize_reply(quote_ranking: Iterable[tuple[str, float]]) -> str:
        quotes, scores = unzip(quote_ranking)
        return choices(quotes, scores)[0]

    @staticmethod
    def choose_best_reply(quote_ranking: Iterable[tuple[str, float]]) -> str:
        return max(quote_ranking, key=lambda quote_and_score: quote_and_score[1])[0]

    def choose_reply(self, quote_ranking: Iterable[tuple[str, float]]) -> str:
        reply = (MasterOfPunchyRetort.randomize_reply(quote_ranking) if self.should_randomize_reply
                 else MasterOfPunchyRetort.choose_best_reply(quote_ranking))
        self.used_quotes.add(reply)
        return reply

    def reply(self, line: str) -> str:
        self.input_line = line
        quote_ranking = self.get_quote_ranking()
        processed_quote_ranking = ((quote, self.process_score(quote, score))
                                   for quote, score in quote_ranking)
        return self.choose_reply(processed_quote_ranking)
