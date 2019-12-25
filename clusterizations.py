"""В этом модули будут распиханные по функция модели кластеризации, а также функции их оценки"""
from os import path
import datetime

from sklearn.cluster import KMeans, AffinityPropagation, AgglomerativeClustering, DBSCAN
import joblib

import metricio


def train_kmean(dict_data, clusters):
    # Кластеризация, использующая алгоритм K-means
    # dict_data - данные для кластеризации {имя объекта:[список признаков]}
    # clusters - результирующее количество кластеров
    # Сохраняет модель на диск и возвращает кластеризацию для обучающего множества
    kmeans = KMeans(n_clusters=clusters)
    keys = dict_data.keys()
    features = [[float(val) for val in value] for value in dict_data.values()]
    features = normalize_data(features)
    result = kmeans.fit_predict(features)
    joblib.dump(kmeans, path.join('models', 'KMeans n_clusters=' + str(clusters) + '.pkl'))
    result = dict(zip(keys, result))
    return result


def train_affinity_propagation(dict_data, preference=None):
    # Кластеризация, использующая алгоритм Affinity Propagation
    # dict_data - данные для кластеризации {имя объекта:[список признаков]}
    # preference - значение, определяющее вероятность точки стать центром кластера.
    # Сохраняет модель на диск и возвращает кластеризацию для обучающего множества
    afprop = AffinityPropagation(preference=preference)
    keys = dict_data.keys()
    features = [[float(val) for val in value] for value in dict_data.values()]
    features = normalize_data(features)
    result = afprop.fit_predict(features)
    joblib.dump(afprop, path.join('models', 'Affinity Propagation preference=' + str(preference) + '.pkl'))
    result = dict(zip(keys, result))
    return result


def train_agglomerative(dict_data, clusters, affinity='euclidean', linkage='ward'):
    # Кластеризация, использующая алгоритм Agglomerative clustering
    # dict_data - данные для кластеризации{имя объекта:[список признаков]}
    # clusters - результирующее количество кластеров, affinity - метика вычисления расстояния между точками
    # linkage - метрика вычисления похожести двух кластеров. Варианты: "ward", "single", "average", "complete"
    # Сохраняет модель на диск и возвращает кластеризацию для обучающего множества
    aggl = AgglomerativeClustering(n_clusters=clusters, affinity=affinity, linkage=linkage)
    keys = dict_data.keys()
    features = [[float(val) for val in value] for value in dict_data.values()]
    features = normalize_data(features)
    result = aggl.fit_predict(features)
    joblib.dump(aggl, path.join('models', 'Agglomerative n_clusters=' + str(
        clusters) + ' affinity=' + affinity + ' linkage=' + linkage + '.pkl'))
    result = dict(zip(keys, result))
    return result


def train_dbscan(dict_data, eps=0.5, min_samples=3):
    # Кластеризация, использующая алгоритм DBSCAN
    # dict_data - данные для кластеризации {имя объекта:[список признаков]}
    # eps - радиус окружности вокруг точки, в которой идет поиск других точек
    # min_samples - количество точек, которое должно быть найдено в этой окружности, чтобы точка не считалась шумом
    # Сохраняет модель на диск и возвращает кластеризацию для обучающего множества
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    keys = dict_data.keys()
    features = [[float(val) for val in value] for value in dict_data.values()]
    features = normalize_data(features)
    result = dbscan.fit_predict(features)
    joblib.dump(dbscan, path.join('models', 'DBSCAN eps=' + str(eps) + ' min_samples=' + str(min_samples) + '.pkl'))
    result = dict(zip(keys, result))
    return result


def save_predictions(result, filename=str(datetime.datetime.now())):
    # Сохраняет результат кластеризации на диск
    result = list(result.items())
    result.sort(key=lambda i: i[1])
    with open(path.join('results', filename), 'w+', encoding='UTF-8') as file:
        for key, value in result:
            file.write(str(value) + ' cluster: ' + key + '\n')


def normalize_data(data):
    # Делает нормализацию данных, приводя значения признаков к промежутку от 0 до 1
    for i in range(len(data[0])):
        max_x = 0
        for x in data:
            if x[i] > max_x:
                max_x = x[i]
        for x in data:
            x[i] = x[i] / max_x
    return data


_, data = metricio.read_metrics('data.txt')
result = train_kmean(data, clusters=91)
save_predictions(result, 'K-mean clusters = 91, normalized')
