class Sentences:
    def __init__(self, stream):
        self.iter = iter(stream)


    def __iter__(self):
        return self


    def __next__(self):
        sentence = ''

        for c in self.iter:
            sentence += c

            if c == '.':
                return sentence

        raise StopIteration


    def correct(sentence):
        corrected = sentence[0].upper() + sentence[1:]

        while corrected[-1].isspace():
            corrected = corrected[:-1]
        if corrected[-1] != '.':
            corrected += '.'

        return corrected


def presentation(stream):
    for sentence in map(Sentences.correct, iter(Sentences(stream))):
        print(sentence)