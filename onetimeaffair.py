"""Здесь будут функции, написанные для одноразового использования"""

import os

from nltk import sent_tokenize, word_tokenize
from rnnmorph.predictor import RNNMorphPredictor

import corpcrawler as crawl
from metriceval import lose_non_russian_alphabet, eval_metric_multithread


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
