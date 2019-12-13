"""В этом модуле будут функции для подгрузке наших результатов обсчета из файлов и сохранения их в файлы"""


def read_metrics(path):
    # Возвращает данные в виде: {объект:[список метрик]}
    with open(path, encoding='UTF-8') as file:
        meta = file.readline().strip().split('|')  # сохраняем строку с метаданными
        data = {line.split(':')[0]: line.split(':')[1].strip('\n|').split('|') for line in file.readlines()}
        return meta, data


def add_new_metric(path, label, metric):
    # Дозаписывет метрику в файл с данными. label - метка метрики, metric - {объект:значение метрики}
    meta, data = read_metrics(path)
    with open(path, 'w', encoding='UTF-8') as file:
        file.write('|'.join(meta) + '|' + label + '\n')
        for key, value in data.items():
            file.write(key + ':' + '|'.join(value) + '|' + str(metric[key]) + '\n')


def change_existed_metric(path, label, metric):
    # Меняет указанную метрику в файле с данными. label - метка метрики, metric - {объект:значение метрики}
    meta, data = read_metrics(path)
    with open(path, 'w', encoding='UTF-8') as file:
        i = meta.index(label)
        file.write('|'.join(meta) + '\n')
        for key, value in data.items():
            value[i] = str(metric[key])
            file.write(key + ':' + '|'.join(value) + '\n')


def add_new_object(path, key, metrics):
    # Добавляет новый объект в конец файла с данными. key - имя объекта, metrics - {метка метрики:значение метрики}
    # Если метрика не посчитана, пишет 0.
    with open(path, 'r+', encoding='UTF-8') as file:
        meta = file.readline().strip().split('|')
        line = [str(metrics[label]) if label in metrics else str(0) for label in meta]
        file.write(key + ':' + '|'.join(line) + '\n')


def change_existed_object(path, key, metrics):
    # Изменяет существующий объект в файле с данными. key - имя объекта, metrics - {метка метрики:значение метрики}
    # Если метрика не посчитана, оставляет старое значение.
    meta, data = read_metrics(path)
    with open(path, 'w', encoding='UTF-8') as file:
        file.write('|'.join(meta) + '\n')
        data[key] = [str(metrics[label]) if label in metrics else data[key][meta.index(label)] for label in meta]
        for key, value in data.items():
            file.write(key + ':' + '|'.join(value) + '\n')


def delete_metric(path, label):
    # Удаляет значения метрики label из файла с данными
    meta, data = read_metrics(path)
    with open(path, 'w', encoding='UTF-8') as file:
        i = meta.index(label)
        meta.remove(label)
        file.write('|'.join(meta) + '\n')
        for key, value in data.items():
            value.pop(i)
            file.write(key + ':' + '|'.join(value) + '\n')

# delete_metric('data.txt', 'advperc')
