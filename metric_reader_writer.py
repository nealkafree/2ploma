"""В этом модуле будут функции для подгрузке наших результатов обсчета из файлов и сохранения их в файлы"""


def read_metrics(path):
    # Возвращает данные в виде: {ключ:[список метрик]}
    with open(path) as file:
        meta = file.readline().strip()  # сохраняем строку с метаданными
        data = {line.split(':')[0]: line.split(':')[1].strip().split('|') for line in file.readlines()}
        return meta, data


def add_new_metric(path, label, metric):
    # Дозаписывет метрику в файл с данными. label - метка метрики, metric - {ключ:значение метрики}
    meta, data = read_metrics(path)
    with open(path, 'w') as file:
        meta = meta + '|' + label + '\n'
        file.write(meta)
        for key, value in data.values():
            string = key + ':' + value.join('|') + '|' + metric[key] + '\n'
            file.write(string)


print(read_metrics('test.txt'))
