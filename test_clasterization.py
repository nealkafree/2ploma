from sklearn.cluster import KMeans
import metric_reader_writer as metricrw

_, data = metricrw.read_metrics('test.txt')
train_data = [[float(k) for k in value] for value in data.values()]
kmeans = KMeans(n_clusters=2)
kmeans.fit(train_data)
print(kmeans.predict([[0, 1, 0], [2, 2, 2], [0, 0, 0]]))
