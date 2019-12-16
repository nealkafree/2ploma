"""В этом модуле будут функции для подсчета метрик"""
import math
from multiprocessing import Pool
import re

from nltk.tokenize import word_tokenize, sent_tokenize
from tqdm import tqdm

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


def percent_of_nouns(key, text):
    # Получает {ключ:текст строкой}. Возвращает процент существительных в тексте. Используется нормализованный корпус.
    # Метка: nounperc
    pos_tags = [word.split(',')[2] for word in text.split('|')]
    noun_count = pos_tags.count('NOUN')
    return key, round(noun_count / len(pos_tags), 5)


def percent_of_verbs(key, text):
    # Получает {ключ:текст строкой}. Возвращает процент глаголов в тексте. Используется нормализованный корпус.
    # Метка: verbperc
    pos_tags = [word.split(',')[2] for word in text.split('|')]
    noun_count = pos_tags.count('VERB')
    return key, round(noun_count / len(pos_tags), 5)


def percent_of_adjectives(key, text):
    # Получает {ключ:текст строкой}. Возвращает процент прилагательных в тексте. Используется нормализованный корпус.
    # Метка: adjperc
    pos_tags = [word.split(',')[2] for word in text.split('|')]
    noun_count = pos_tags.count('ADJ')
    return key, round(noun_count / len(pos_tags), 5)


def percent_of_pronouns(key, text):
    # Получает {ключ:текст строкой}. Возвращает процент местоимений в тексте. Используется нормализованный корпус.
    # Метка: pronperc
    pos_tags = [word.split(',')[2] for word in text.split('|')]
    noun_count = pos_tags.count('PRON')
    return key, round(noun_count / len(pos_tags), 5)


def percent_of_conjugations(key, text):
    # Получает {ключ:текст строкой}. Возвращает процент союзов в тексте. Используется нормализованный корпус.
    # Метка: conjperc
    pos_tags = [word.split(',')[2] for word in text.split('|')]
    noun_count = pos_tags.count('CONJ')
    return key, round(noun_count / len(pos_tags), 5)


def text_entropy(key, text):
    # Получает {ключ:текст строкой}. Возвращает энтропию текста. Используется нормализованный корпус.
    # Метка: entropy
    normalized_words = [word.split(',')[1] for word in text.split('|')]
    freq_dict = {}
    for word in normalized_words:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    entropy = 0
    n = len(normalized_words)
    for _, value in freq_dict.items():
        entropy += (value / n) * math.log2(value / n)
    return key, round(-entropy, 5)


def text_surprisal(key, text):
    # Получает {ключ:текст строкой}. Возвращает метрику surprisal текста. Используется нормализованный корпус.
    # Метка: surprisal
    normalized_context = [word.split(',')[1] for word in text.split('|')]
    normalized_words = normalized_context[1:]
    freq_dict = {}
    bigr_freq_dict = {}
    for context, word in zip(normalized_context, normalized_words):
        if context in freq_dict:
            freq_dict[context] += 1
        else:
            freq_dict[context] = 1
        if (context, word) in bigr_freq_dict:
            bigr_freq_dict[(context, word)] += 1
        else:
            bigr_freq_dict[(context, word)] = 1
    surprisal = 0
    n = len(normalized_words)
    for (context, word), value in bigr_freq_dict.items():
        surprisal += math.log2(freq_dict[context] / value)
    return key, round(surprisal / len(bigr_freq_dict), 5)


def lose_non_russian_alphabet(text):
    # Удаляет из текста любые символы не являющиеся кириллицей
    return re.sub('[^а-яА-ЯёЁ]', '', text)


if __name__ == '__main__':
    result = eval_metric_multithread(func=text_surprisal, data=crawl.get_texts('Normalized Corpus'))
    metricio.change_existed_metric('data.txt', 'surprisal', result)

