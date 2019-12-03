"""В этом модуле будут функции для подсчета метрик"""

from nltk.tokenize import word_tokenize, sent_tokenize
import corpus_crawler as crawl
import metric_reader_writer as metricrw


def avg_words_in_sentence(text):
    # Получает текст строкой. Возвращает среднее количество слов в предложении.
    # Метка: avgwordsen
    sent_count = 0
    word_count = 0
    for sentence in sent_tokenize(text):
        if len(sentence) > 1:
            sent_count += 1
            for word in word_tokenize(sentence):
                if word.isalpha():
                    word_count += 1
    return word_count / sent_count


# data = crawl.get_texts('Corpus')
# metric = {}
# for key, value in data.items():
#     metric[key] = avg_words_in_sentence(value)
# metricrw.add_new_metric('data.txt', 'avgwordsen', metric)
