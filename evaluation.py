"""В этом модуле будут функции и данные для оценки качества работы моделей"""

import clusterizations
import metricio


def measure_objects_linkage(data):
    # Создает словарь, в котором каждому произведению сопоставляются произведения,
    # с которыми оно попадает в один кластер и количество этих попаданий по нескольким моделям
    # data - {название произведения: набор признаков}
    results = [clusterizations.train_kmean(data, 7), clusterizations.train_kmean(data, 31),
               clusterizations.train_kmean(data, 91), clusterizations.train_affinity_propagation(data, preference=None),
               clusterizations.train_affinity_propagation(data, preference=-50),
               clusterizations.train_affinity_propagation(data, preference=-2),
               clusterizations.train_agglomerative(data, 7), clusterizations.train_agglomerative(data, 31),
               clusterizations.train_agglomerative(data, 91)]
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

# for key, value in cluster_linkage.items():
#     strict = False
#     for linked, measure in value.items():
#         if measure > 4:
#             strict = True
#     if not strict:
#         print(key)
