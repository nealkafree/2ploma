"""Здесь будут функции, написанные для одноразового использования"""

import os
import re

from nltk import sent_tokenize, word_tokenize
from rnnmorph.predictor import RNNMorphPredictor
from tqdm import tqdm

import corpcrawler as crawl
import metricio
from metriceval import lose_non_russian_alphabet, eval_metric_multithread
import clusterizations


def create_base_for_data(path):
    data = crawl.get_texts('Corpus')
    with open(path, 'w', encoding='UTF-8') as file:
        file.write('\n')
        for key, value in data.items():
            file.write(key + ':' + '\n')


def implement_normalization(key, text):
    predictor = RNNMorphPredictor(language='ru')
    word_morph = []
    for sentence in sent_tokenize(text):
        words = [lose_non_russian_alphabet(word).lower() for word in word_tokenize(sentence) if
                 lose_non_russian_alphabet(word).isalpha()]
        if len(words) > 0:
            word_morph += predictor.predict(words)
    word_morph = [str(word.word) + ',' + str(word.normal_form) + ',' + str(word.pos) for word in word_morph]
    return key, '|'.join(word_morph)


def create_normalized_corpus(path):
    result = eval_metric_multithread(func=implement_normalization, data=crawl.get_texts('Corpus'), t=8)
    for key, value in result.items():
        with open(os.path.join(path, key), 'w', encoding='UTF-8') as file:
            file.write(value)


def transliterate(path):
    _, books = metricio.read_metrics(path)
    books = [book.lower() for book in books.keys()]

    with open('Список произведений.txt', 'w', encoding='UTF-8') as file:
        for book in books:
            book = re.sub('shch', 'щ', book)
            book = re.sub('ie', 'е', book)
            book = re.sub('_', 'ь', book)
            book = re.sub('gh', 'г', book)
            book = re.sub('ts', 'ц', book)
            book = re.sub('ia', 'я', book)
            book = re.sub('iu', 'ю', book)
            book = re.sub('zh', 'ж', book)
            book = re.sub('ch', 'ч', book)
            book = re.sub('sh', 'ш', book)
            book = re.sub('kh', 'х', book)
            book = re.sub('hn', 'н', book)
            book = re.sub('ph', 'п', book)
            book = re.sub('j', 'дж', book)
            book = re.sub('a', 'а', book)
            book = re.sub('b', 'б', book)
            book = re.sub('v', 'в', book)
            book = re.sub('d', 'д', book)
            book = re.sub('g', 'г', book)
            book = re.sub('z', 'з', book)
            book = re.sub('i', 'и', book)
            book = re.sub('k', 'к', book)
            book = re.sub('l', 'л', book)
            book = re.sub('m', 'м', book)
            book = re.sub('n', 'н', book)
            book = re.sub('o', 'о', book)
            book = re.sub('p', 'п', book)
            book = re.sub('r', 'р', book)
            book = re.sub('s', 'с', book)
            book = re.sub('t', 'т', book)
            book = re.sub('u', 'у', book)
            book = re.sub('f', 'ф', book)
            book = re.sub('y', 'ы', book)
            book = re.sub('e', 'э', book)
            file.write(book + '\n')


def count_words(key, text_path):
    with open(text_path, encoding='UTF-8') as file:
        text = file.read()
    word_count = 0
    for word in word_tokenize(text):
        word = lose_non_russian_alphabet(word)
        if word.isalpha():
            word_count += 1
    return key, word_count


def delete_short(path):
    texts = []
    for r, d, f in os.walk(path):
        for file in f:
            filename = os.path.join(r, file)
            if os.path.isfile(filename):
                texts.append(filename)
    result = eval_metric_multithread(func=count_words, data={text: text for text in texts}, t=8)
    for file, count in result.items():
        if count < 2000:
            os.remove(file)


if __name__ == '__main__':
    delete_short('GenreCorpus_updating')
