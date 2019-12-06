"""В этом модуле будут функции для подсчета метрик"""

from multiprocessing import Pool
import re

from nltk.tokenize import word_tokenize, sent_tokenize
from tqdm import tqdm
from rnnmorph.predictor import RNNMorphPredictor

import corpcrawler as crawl
import metricio

VOWELS = {"у", "е", "ы", "а", "о", "э", "я", "и", "ю", "ё"}


def eval_metric_multithread(func, data, t=None):
    # Получает функцию и словарь с данными. Создает пул процессов для вычисления функции многопоточно.
    # func - функция, data - {ключ:данные для вычисления}, t - количество процессов, которые будут проводить вычисления.
    # Возвращает {ключ:результат вычисления}
    p = Pool(t)
    pool_results = [p.apply_async(func, (key, value)) for key, value in data.items()]
    results = dict(res.get() for res in tqdm(pool_results))
    p.close()
    p.join()
    return results


def avg_words_in_sentence(key, text):
    # Получает {ключ:текст строкой}. Возвращает среднее количество слов в предложении.
    # Метка: avgwordsen
    sent_count = 0
    word_count = 0
    for sentence in sent_tokenize(text):
        with_word = False
        for word in word_tokenize(sentence):
            word = lose_non_russian_alphabet(word)
            if word.isalpha():
                word_count += 1
                with_word = True
        if with_word:
            sent_count += 1
    return key, round(word_count / sent_count, 5)


def avg_char_in_word(key, text):
    # Получает {ключ:текст строкой}. Возвращает среднее количество букв в слове.
    # Метка: avgchrword
    char_count = 0
    word_count = 0
    for word in word_tokenize(text):
        word = lose_non_russian_alphabet(word)
        if word.isalpha():
            word_count += 1
            char_count += len(word)
    return key, round(char_count / word_count, 5)


def avg_syl_in_word(key, text):
    # Получает {ключ:текст строкой}. Возвращает среднее количество слогов в слове.
    # Метка: avgsylword
    syl_count = 0
    word_count = 0
    for word in word_tokenize(text):
        word = lose_non_russian_alphabet(word)
        with_syllable = False
        for char in word.lower():
            if char in VOWELS:
                syl_count += 1
                with_syllable = True
        if with_syllable:
            word_count += 1
    return key, round(syl_count / word_count, 5)


def percent_of_pos(key, text):
    # Получает {ключ:текст строкой}. Возвращает процент существительных в тексте.
    # Метка: nounperc, verbperc, pronperc, adjperc, advperc, conjperc
    predictor = RNNMorphPredictor(language='ru')
    words = [lose_non_russian_alphabet(word) for word in word_tokenize(text) if
             lose_non_russian_alphabet(word).isalpha()]
    word_morph = predictor.predict(words)
    nouns_count = 0
    verbs_count = 0
    adjectives_count = 0
    pronouns_count = 0
    adverbs_count = 0
    conjunctions_count = 0
    for morph in word_morph:
        if morph.pos == 'NOUN':
            nouns_count += 1
        elif morph.pos == 'VERB':
            verbs_count += 1
        elif morph.pos == 'PRON':
            pronouns_count += 1
        elif morph.pos == 'ADJ':
            adjectives_count += 1
        elif morph.pos == 'ADV':
            adverbs_count += 1
        elif morph.pos == 'CONJ':
            conjunctions_count += 1
    if nouns_count == 0:
        print(key)
    return key, [round(nouns_count / len(words), 5), round(verbs_count / len(words), 5),
                 round(pronouns_count / len(words), 5), round(adjectives_count / len(words), 5),
                 round(adverbs_count / len(words), 5), round(conjunctions_count / len(words), 5)]


def lose_non_russian_alphabet(text):
    # Удаляет из текста любые символы не являющиеся кириллицей
    return re.sub('[^а-яА-ЯёЁ]', '', text)


if __name__ == '__main__':
    result = eval_metric_multithread(func=percent_of_pos, data=crawl.get_texts('Corpus'), t=4)
    metricio.add_new_metric('data.txt', 'nounperc', {key: value[0] for key, value in result.items()})
    metricio.add_new_metric('data.txt', 'verbperc', {key: value[1] for key, value in result.items()})
    metricio.add_new_metric('data.txt', 'pronperc', {key: value[2] for key, value in result.items()})
    metricio.add_new_metric('data.txt', 'adjperc', {key: value[3] for key, value in result.items()})
    metricio.add_new_metric('data.txt', 'advperc', {key: value[4] for key, value in result.items()})
    metricio.add_new_metric('data.txt', 'conjperc', {key: value[5] for key, value in result.items()})

