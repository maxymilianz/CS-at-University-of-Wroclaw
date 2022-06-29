from interlocutor import InputInterlocutor, Interlocutor, MasterOfPunchyRetort
from lemmatizer import MorfologikLemmatizer
from utilities import load_quotes


def append_to_file(contents: str, path: str):
    with open(path, 'a', encoding='utf8') as file:
        file.write(contents)


def conversate(interlocutor_0: Interlocutor,
               interlocutor_1: Interlocutor,
               path_to_save: str = 'dialogue.txt',
               max_length: int = 1000,
               initial_line: str = ''):
    line_1 = initial_line

    for _ in range(max_length):
        line_0 = interlocutor_0.reply(line_1)
        append_to_file(f'0: {line_0}\n', path_to_save)
        line_1 = interlocutor_1.reply(line_0)
        append_to_file(f'1: {line_1}\n', path_to_save)


def main():
    input_interlocutor = InputInterlocutor()
    quotes = load_quotes('mini_quotes.txt')
    lemmatizer = MorfologikLemmatizer('../polimorfologik-2.1.txt')
    master_of_punchy_retort = MasterOfPunchyRetort(quotes, lemmatizer, should_randomize_reply=True)
    conversate(input_interlocutor, master_of_punchy_retort)


if __name__ == '__main__':
    main()
