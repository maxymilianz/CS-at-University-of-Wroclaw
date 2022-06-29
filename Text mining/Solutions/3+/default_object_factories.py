from article_presenter.abstract_article_presenter import AbstractArticlePresenter
from article_presenter.article_presenter import ArticlePresenter
from article_presenter.phrasal_article_presenter import PhrasalArticlePresenter
from corrector.corrector import Corrector
from corrector.sluggy_corrector import SluggyCorrector
from definition import Definition, load_definitions_from_articles, load_definitions_from_wiktionary
from index_manager.abstract_index_manager import IndexManager
from index_manager.file_index_manager import FileIndexManager
from lemmatizer import Lemmatizer, MorfologikLemmatizer
from position_to_article_mapper import FilePositionToArticleMapper, PositionToArticleMapper
from question_answerer.abstract_question_answerer import AbstractQuestionAnswerer
from question_answerer.adage_question_answerer import AdageQuestionAnswerer
from question_answerer.affirmative_question_answerer import AffirmativeQuestionAnswerer
from question_answerer.generic_question_answerer import GenericQuestionAnswerer
from question_answerer.human_name_question_answerer import HumanNameQuestionAnswerer
from question_answerer.name_question_answerer import NameQuestionAnswerer
from question_answerer.question_answerer import QuestionAnswerer
from question_answerer.year_question_answerer import YearQuestionAnswerer
from search_engine.abstract_search_engine import AbstractSearchEngine
from search_engine.one_title_search_engine import OneTitleSearchEngine
from search_engine.phrasal_search_engine import PhrasalSearchEngine
from search_engine.search_engine import MatchRating, SearchEngine
from similar_definition_finder.cosine_embedding_similar_definition_finder import CosineEmbeddingSimilarDefinitionFinder
from similar_definition_finder.cosine_tf_idf_similar_definition_finder import CosineTfIdfSimilarDefinitionFinder
from similar_definition_finder.similar_definition_finder import SimilarDefinitionFinder
from tokenizer import ExtractWordsTokenizer, Tokenizer
from typo_finder import MorfologikTypoFinder, TypoFinder
from wikipedia_io import WikipediaIo, WikipediaFileIo

from collections.abc import Collection, Iterable
from enum import Enum
from functools import cache


@cache
def get_morfologik_lemmatizer() -> Lemmatizer:
    return MorfologikLemmatizer('resources/polimorfologik-2.1.txt')


@cache
def get_position_to_article_mapper() -> PositionToArticleMapper:
    return FilePositionToArticleMapper('resources/first_positions.txt')


@cache
def get_wikipedia_file_io() -> WikipediaIo:
    return WikipediaFileIo('resources/small_wikipedia.txt')


@cache
def get_article_presenter(phrasal: bool) -> AbstractArticlePresenter:
    lemmatizer = get_morfologik_lemmatizer()
    return (PhrasalArticlePresenter(lemmatizer) if phrasal
            else ArticlePresenter(lemmatizer))


@cache
def get_match_rating() -> MatchRating:
    article_count = get_wikipedia_file_io().get_last_article_id()
    lemmatizer = get_morfologik_lemmatizer()
    return MatchRating(article_count, lemmatizer)


@cache
def get_file_index_manager(positional: bool) -> IndexManager:
    if positional:
        return FileIndexManager('resources/positional_index.txt', 'resources/positional_index_offsets.txt')
    else:
        return FileIndexManager('resources/index.txt', 'resources/offsets.txt')


@cache
def get_search_engine(phrasal: bool) -> AbstractSearchEngine:
    if phrasal:
        lemmatizer = get_morfologik_lemmatizer()
        index_manager = get_file_index_manager(positional=phrasal)
        position_to_article_mapper = get_position_to_article_mapper()
        wikipedia_io = get_wikipedia_file_io()
        return PhrasalSearchEngine(lemmatizer, index_manager, position_to_article_mapper, wikipedia_io)
    else:
        lemmatizer = get_morfologik_lemmatizer()
        index_manager = get_file_index_manager(positional=phrasal)
        wikipedia_io = get_wikipedia_file_io()
        match_rating = get_match_rating()
        return SearchEngine(lemmatizer, index_manager, wikipedia_io, match_rating)


@cache
def get_extract_words_tokenizer() -> Tokenizer:
    return ExtractWordsTokenizer()


@cache
def get_generic_question_answerer(phrasal: bool) -> AbstractQuestionAnswerer:
    search_engine = get_search_engine(phrasal)
    tokenizer = get_extract_words_tokenizer()
    return GenericQuestionAnswerer(search_engine, tokenizer)


@cache
def get_affirmative_question_answerer() -> AbstractQuestionAnswerer:
    return AffirmativeQuestionAnswerer()


@cache
def get_year_question_answerer(phrasal: bool) -> AbstractQuestionAnswerer:
    tokenizer = get_extract_words_tokenizer()
    search_engine = get_search_engine(phrasal)
    return YearQuestionAnswerer(tokenizer, search_engine)


@cache
def get_human_name_question_answerer(phrasal: bool) -> AbstractQuestionAnswerer:
    tokenizer = get_extract_words_tokenizer()
    search_engine = get_search_engine(phrasal)
    return HumanNameQuestionAnswerer(tokenizer, search_engine)


@cache
def get_wiktionary_definitions() -> Collection[Definition]:
    return load_definitions_from_wiktionary('resources/plwiktionary.txt')


@cache
def get_small_wikipedia_definitions() -> Collection[Definition]:
    wikipedia_io = get_wikipedia_file_io()
    return load_definitions_from_articles(wikipedia_io.get_all_articles())


class DefinitionSource(Enum):
    WIKTIONARY = 0
    SMALL_WIKIPEDIA = 1


@cache
def get_cosine_tf_idf_similar_definition_finder(definition_source: DefinitionSource) -> SimilarDefinitionFinder:
    lemmatizer = get_morfologik_lemmatizer()
    definitions = (get_wiktionary_definitions() if definition_source == DefinitionSource.WIKTIONARY
                   else get_small_wikipedia_definitions())
    return CosineTfIdfSimilarDefinitionFinder(lemmatizer, definitions)


@cache
def get_cosine_embedding_similar_definition_finder(definition_source: DefinitionSource) -> SimilarDefinitionFinder:
    lemmatizer = get_morfologik_lemmatizer()
    definitions = (get_wiktionary_definitions() if definition_source == DefinitionSource.WIKTIONARY
                   else get_small_wikipedia_definitions())
    return CosineEmbeddingSimilarDefinitionFinder(lemmatizer, definitions, 'resources/word2vec_100_3_polish.bin')


@cache
def get_name_question_answerer(definition_source: DefinitionSource) -> AbstractQuestionAnswerer:
    # similar_definition_finder = get_cosine_tf_idf_similar_definition_finder(definition_source)
    similar_definition_finder = get_cosine_embedding_similar_definition_finder(definition_source)
    return NameQuestionAnswerer(similar_definition_finder)


@cache
def get_question_answerer(phrasal: bool, definition_source: DefinitionSource) -> AbstractQuestionAnswerer:
    generic_question_answerer = get_generic_question_answerer(phrasal)
    affirmative_question_answerer = get_affirmative_question_answerer()
    year_question_answerer = get_year_question_answerer(phrasal)
    human_name_question_answerer = get_human_name_question_answerer(phrasal)
    name_question_answerer = get_name_question_answerer(definition_source)
    return QuestionAnswerer(generic_question_answerer, [affirmative_question_answerer,
                                                        year_question_answerer,
                                                        human_name_question_answerer,
                                                        name_question_answerer])


@cache
def get_morfologik_typo_finder() -> TypoFinder:
    return MorfologikTypoFinder('resources/polimorfologik-2.1.txt')


@cache
def get_morfologik_words() -> Iterable[str]:
    with open('resources/polimorfologik-2.1.txt', encoding='utf8') as file:
        return (line.split(';')[1] for line in file.readlines())


@cache
def get_small_wikipedia_titles() -> Iterable[str]:
    wikipedia_io = get_wikipedia_file_io()
    return (article.title for article in wikipedia_io.get_all_articles())


class WordSource(Enum):
    MORFOLOGIK = 0
    SMALL_WIKIPEDIA = 1


@cache
def get_corrector(word_source: WordSource) -> Corrector:
    if word_source == WordSource.MORFOLOGIK:
        return SluggyCorrector(get_morfologik_words())
    elif word_source == WordSource.SMALL_WIKIPEDIA:
        return SluggyCorrector(get_small_wikipedia_titles())


@cache
def get_one_title_search_engine() -> AbstractSearchEngine:
    wikipedia_io = WikipediaFileIo('resources/4_1_small_wikipedia.txt')
    return OneTitleSearchEngine(wikipedia_io.get_all_articles())


@cache
def get_adages(path: str) -> Collection[str]:
    with open(path, encoding='utf8') as file:
        return file.readlines()


@cache
def get_adage_question_answerer() -> AbstractQuestionAnswerer:
    adages = get_adages('resources/bootleg_adages.txt')
    return AdageQuestionAnswerer(adages)
