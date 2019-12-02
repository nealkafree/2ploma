"""В этом модуле будут функции для подгрузке наших результатов обсчета из файлов и сохранения их в файлы"""


def read_metrics(path):
    # Возвращает данные в виде: {объект:[список метрик]}
    with open(path, encoding='UTF-8') as file:
        meta = file.readline().strip().split('|')  # сохраняем строку с метаданными
        data = {line.split(':')[0]: line.split(':')[1].strip().split('|') for line in file.readlines()}
        return meta, data


def add_new_metric(path, label, metric):
    # Дозаписывет метрику в файл с данными. label - метка метрики, metric - {объект:значение метрики}
    meta, data = read_metrics(path)
    with open(path, 'w', encoding='UTF-8') as file:
        file.write('|'.join(meta) + '|' + label + '\n')
        for key, value in data.items():
            file.write(key + ':' + '|'.join(value) + '|' + metric[key] + '\n')


def change_existed_metric(path, label, metric):
    # Меняет указанную метрику в файле с данными. label - метка метрики, metric - {объект:значение метрики}
    meta, data = read_metrics(path)
    with open(path, 'w', encoding='UTF-8') as file:
        i = meta.index(label)
        file.write('|'.join(meta) + '\n')
        for key, value in data.items():
            value[i] = metric[key]
            file.write(key + ':' + '|'.join(value) + '\n')


def add_new_object(path, key, metrics):
    # Добавляет новый объект в конец файла с данными. key - имя объекта, metrics - {метка метрики:значение метрики}
    with open(path, 'a', encoding='UTF-8') as file:
        meta = file.readline().strip().split('|')
        line = [metrics[label] if label in metrics else 0 for label in meta]
        file.write(key + ':' + '|'.join(line) + '\n')


change_existed_metric('test.txt', 'tst2', {'test1': 'four', 'test2': 'cuatro'})
