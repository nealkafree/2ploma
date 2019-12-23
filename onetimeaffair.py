"""Здесь будут функции, написанные для одноразового использования"""

import os

from nltk import sent_tokenize, word_tokenize
from rnnmorph.predictor import RNNMorphPredictor

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


def measure_objects_linkage(data):
    results = [clusterizations.train_kmean(data, 7), clusterizations.train_kmean(data, 31),
               clusterizations.train_kmean(data, 91), clusterizations.train_affinity_propagation(data, preference=None),
               clusterizations.train_affinity_propagation(data, preference=-50),
               clusterizations.train_affinity_propagation(data, preference=-2),
               clusterizations.train_agglomerative(data, 7), clusterizations.train_agglomerative(data, 31),
               clusterizations.train_agglomerative(data, 91)]
               # clusterizations.train_agglomerative(data, 7, linkage='average'),
               # clusterizations.train_agglomerative(data, 31, linkage='average'),
               # clusterizations.train_agglomerative(data, 91, linkage='average'),
               # clusterizations.train_agglomerative(data, 7, linkage='complete'),
               # clusterizations.train_agglomerative(data, 31, linkage='complete'),
               # clusterizations.train_agglomerative(data, 91, linkage='complete'),
               # clusterizations.train_dbscan(data, eps=0.5), clusterizations.train_dbscan(data, eps=0.7)]
    linkage = {}
    for key, value in data.items():
        links = {}
        for result in results:
            clas_obj = result[key]
            for pred_key, clas in result.items():
                if (clas == clas_obj) and not (pred_key == key):
                    if pred_key in links:
                        links[pred_key] += 1
                    else:
                        links[pred_key] = 1
        linkage[key] = links
    return linkage


_, data = metricio.read_metrics('data.txt')
cluster_linkage = measure_objects_linkage(data)

# printed = set()
# for key, value in cluster_linkage.items():
#     if key not in printed:
#         print(key)
#         for linked, measure in value.items():
#             if measure == 9:
#                 print(linked)
#                 printed.add(linked)
#         printed.add(key)
#         print()

for key, value in cluster_linkage.items():
    strict = False
    for linked, measure in value.items():
        if measure > 4:
            strict = True
    if not strict:
        print(key)
