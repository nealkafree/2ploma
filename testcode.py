from multiprocessing import Pool
from os import path

from sklearn.cluster import KMeans
from rnnmorph.predictor import RNNMorphPredictor
from nltk.tokenize import word_tokenize
import joblib

import metricio

# _, data = metricio.read_metrics('data.txt')
# train_data = [[float(k) for k in value] for value in data.values()]
# kmeans = KMeans(n_clusters=7)
# kmeans.fit(train_data)
# result = [(key, kmeans.predict([[float(val) for val in value]])) for key, value in data.items()]
# result.sort(key=lambda i: i[1])

# with open('Разбивка на классы, Kmeans, компоненты readability.txt', 'w+', encoding='UTF-8') as file:
#     for text in result:
#         file.write(str(text) + '\n')

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
# with open('Минутка философии', encoding='UTF-8') as file:
#     print(predictor.predict(word_tokenize(file.read())))

# clf = joblib.load(path.join('models', 'KMeans n_clusters=31.pkl'))
# vec = range(10)
# print(clf.predict([vec]))
