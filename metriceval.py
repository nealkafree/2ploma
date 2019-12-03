"""В этом модуле будут функции для подсчета метрик"""

from multiprocessing import Pool

from nltk.tokenize import word_tokenize, sent_tokenize

import corpcrawler as crawl
import metricio


def avg_words_in_sentence(cort):
    # Получает текст строкой. Возвращает среднее количество слов в предложении.
    # Метка: avgwordsen
    sent_count = 0
    word_count = 0
    for sentence in sent_tokenize(cort[1]):
        if len(sentence) > 1:
            sent_count += 1
            for word in word_tokenize(sentence):
                if word.isalpha():
                    word_count += 1
    return cort[0], round(word_count / sent_count, 5)


# data = crawl.get_texts('Corpus')
# if __name__ == '__main__':
#     p = Pool()
#     test = p.map(avg_words_in_sentence, data.items())
#     # for key, value in data.items():
#     #     metric[key] = avg_words_in_sentence(value)
#     p.close()
#     p.join()
#     metricio.change_existed_metric('data.txt', 'avgwordsen', dict(test))
