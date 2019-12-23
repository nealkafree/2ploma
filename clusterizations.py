"""В этом модули будут распиханные по функция модели кластеризации, а также функции их оценки"""
from os import path
import datetime

from sklearn.cluster import KMeans, AffinityPropagation, AgglomerativeClustering, DBSCAN
import joblib

import metricio


def train_kmean(dict_data, clusters):
    kmeans = KMeans(n_clusters=clusters)
    keys = dict_data.keys()
    result = kmeans.fit_predict([[float(val) for val in value] for value in dict_data.values()])
    joblib.dump(kmeans, path.join('models', 'KMeans n_clusters=' + str(clusters) + '.pkl'))
    result = dict(zip(keys, result))
    return result


def train_affinity_propagation(dict_data, preference=None):
    afprop = AffinityPropagation(preference=preference)
    keys = dict_data.keys()
    result = afprop.fit_predict([[float(val) for val in value] for value in dict_data.values()])
    joblib.dump(afprop, path.join('models', 'Affinity Propagation preference=' + str(preference) + '.pkl'))
    result = dict(zip(keys, result))
    return result


def train_agglomerative(dict_data, clusters, affinity='euclidean', linkage='ward'):
    aggl = AgglomerativeClustering(n_clusters=clusters, affinity=affinity, linkage=linkage)
    keys = dict_data.keys()
    result = aggl.fit_predict([[float(val) for val in value] for value in dict_data.values()])
    joblib.dump(aggl, path.join('models', 'Agglomerative n_clusters=' + str(clusters) + ' affinity=' + affinity + ' linkage=' + linkage + '.pkl'))
    result = dict(zip(keys, result))
    return result


def train_dbscan(dict_data, eps=0.5, min_samples=3):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    keys = dict_data.keys()
    result = dbscan.fit_predict([[float(val) for val in value] for value in dict_data.values()])
    joblib.dump(dbscan, path.join('models', 'DBSCAN eps=' + str(eps) + ' min_samples=' + str(min_samples) + '.pkl'))
    result = dict(zip(keys, result))
    return result


def save_predictions(result, filename=str(datetime.datetime.now())):
    result.sort(key=lambda i: i[1])
    with open(path.join('results', filename), 'w+', encoding='UTF-8') as file:
        for key, value in result:
            file.write(str(value) + ' cluster: ' + key + '\n')


# _, data = metricio.read_metrics('data.txt')
# result = train_affinity_propagation(data, preference=-2)
# save_predictions(result, 'Affinity Propagation preference=-2')
