"""Здесь будут функции, написанные для одноразового использования"""

import corpus_crawler as crawl


def create_base_for_data(path):
    data = crawl.get_texts('Corpus')
    with open(path, 'w', encoding='UTF-8') as file:
        file.write('\n')
        for key, value in data.items():
            file.write(key + ':' + '\n')


create_base_for_data('data.txt')
