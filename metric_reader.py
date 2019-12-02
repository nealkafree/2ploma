"""В этом модуле будут функции для подгрузке наших результатов обсчета из файлов"""


def read_metrics(path):
    # Возвращает данные в виде: {ключ:[список метрик]}
    with open(path) as file:
        file.readline()  # пропускаем первую строку с метаданными

        data = {line.split(':')[0]: line.split(':')[1].strip().split('|') for line in file.readlines()}
        return data


print(read_metrics('test.txt'))
