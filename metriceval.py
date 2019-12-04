"""В этом модуле будут функции для подсчета метрик"""

from multiprocessing import Pool
import re

from nltk.tokenize import word_tokenize, sent_tokenize
from tqdm import tqdm

import corpcrawler as crawl
import metricio


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
    # Получает текст строкой. Возвращает среднее количество слов в предложении.
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
    # Получает текст строкой. Возвращает среднее количество букв в слове.
    # Метка avgchrword
    char_count = 0
    word_count = 0
    for word in word_tokenize(text):
        word = lose_non_russian_alphabet(word)
        if word.isalpha():
            word_count += 1
            char_count += len(word)
    return key, round(char_count / word_count, 5)


def lose_non_russian_alphabet(text):
    # Удаляет из текста любые символы не являющиеся кириллицей
    return re.sub('[^а-яА-ЯёЁ]', '', text)


# if __name__ == '__main__':
#     metricio.add_new_metric('data.txt', 'avgchrword',
#                             eval_metric_multithread(func=avg_char_in_word, data=crawl.get_texts('Corpus')))
