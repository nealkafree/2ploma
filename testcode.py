from multiprocessing import Pool

from sklearn.cluster import KMeans
from rnnmorph.predictor import RNNMorphPredictor
from nltk.tokenize import word_tokenize

import metricio

# _, data = metricio.read_metrics('data.txt')
# train_data = [[float(k) for k in value] for value in data.values()]
# kmeans = KMeans(n_clusters=7)
# kmeans.fit(train_data)
# result = [(key, kmeans.predict([value])) for key, value in data.items()]
# result.sort(key=lambda i: i[1])
# print(*result)


#
# if __name__ == '__main__':
#     p = Pool()
#     test = {1: 1, 2: 2, 3: 4, 5: 1, 4: 6}
#     test = p.map(mul, test.items())
#     print(test)
#     p.close()
#     p.join()

# test = [(1,2), (2,3)]
# t =dict(test)
# print(t)

# predictor = RNNMorphPredictor(language='ru')
