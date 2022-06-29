class Typo:
    def __init__(self, actual_word: str, correct_word: str):
        self.actual_word = actual_word
        self.correct_word = correct_word


class Corrector:
    def correct(self, word: str) -> str:
        raise NotImplementedError
