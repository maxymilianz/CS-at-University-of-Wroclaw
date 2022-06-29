from index_manager import FileIndexManager
from lemmatizer import MorfologikLemmatizer
from search_engine import MatchRating, SearchEngine
from wikipedia_io import WikipediaFileIo

import spacy
import editdistance
from itertools import product


lemmatizer = MorfologikLemmatizer('../polimorfologik-2.1.txt')
index_manager = FileIndexManager('../2/index.txt', '../2/offsets.txt')
wikipedia_io = WikipediaFileIo('../2/small_wikipedia.txt')
match_rating = MatchRating(wikipedia_io.get_last_article_id(), lemmatizer)

search_engine = SearchEngine(lemmatizer, index_manager, wikipedia_io, match_rating)


def search_titles(query):
    articles = search_engine.search(query)
    return [article.title for article in articles]


spacy_model = spacy.load("pl_core_news_sm")


def scaled_editdist(ans, cor):
    ans = ans.lower()
    cor = cor.lower()

    return editdistance.eval(ans, cor) / len(cor)


def answer(question):
    sm = spacy_model(question)
    question_tokens = [token for token in sm if len(token) > 1]
    while question_tokens:
        query = ' '.join(q.text for q in question_tokens)
        search_results = search_titles(query)

        for result in search_results:
            res_tokens = spacy_model(result)

            for t1, t2 in product(res_tokens, question_tokens):
                if scaled_editdist(t1.text, t2.text) <= 0.5:
                    break
            else:
                paren_index = result.find('(')
                if paren_index != -1:
                    result = result[:paren_index]
                return result

        # if answer not found, remove first token of query
        del question_tokens[0]
    return 'nie mam pojęcia, sorry'


def write_to_file(reply: str, path: str):
    with open(path, 'a+', encoding='utf8') as file:
        file.write(f'{reply}\n')


if __name__ == '__main__':
    for q in open("few_questions.txt", encoding='utf8'):
        q = q.strip()
        print(q)
        reply = answer(q)
        write_to_file(reply, 'answers.txt')
        print(answer(q))
        print()
