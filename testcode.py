from sklearn.cluster import KMeans
import metric_reader_writer as metricrw
from multiprocessing import Pool


# _, data = metricrw.read_metrics('test.txt')
# train_data = [[float(k) for k in value] for value in data.values()]
# kmeans = KMeans(n_clusters=2)
# kmeans.fit(train_data)
# print(kmeans.predict([[0, 1, 0], [2, 2, 2], [0, 0, 0]]))

# def mul(k):
#     return k[0], k[0] * k[1]
#
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