from string import punctuation
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

from NLP.CSVmodule import *
from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2
import nltk
from functools import reduce
import re
from NLP.read_write import *
import numpy as np
from scipy.spatial.distance import *


def max_score(words: []):
    value_max = words[0].score
    index_max = 0
    for i in range(1, len(words)):
        if words[i].score > value_max:
            value_max = words[i].score
            index_max = i
    return index_max


nltk.download('stopwords')
# Загружаем стоп-слова + дополнительные
new_stopwords = stopwords.words('russian') + ['из-за', 'который', 'около']

# Загружаем пунктцацию + дополнительные
new_punctuation = [pun for pun in punctuation] + ["''", '``', '–']

# Считываем данные из датасета
data = csv_reader('data_society_2020.csv')

# Выбираем заголовки статей
text = [dat[3] for dat in data]

# Разбиваем заголовки на токены (слова)
words = [nltk.word_tokenize(sentence) for sentence in text]

# Подключаем морфемный анализатор
morph = pymorphy2.MorphAnalyzer()

# Приводим каждое слово к нормальной форме
result = []
for sentence in words:
    row = []
    for word in sentence:

        temp = morph.parse(word)
        word_max = temp[max_score(temp)]
        if word_max.tag.POS in {'NOUN', 'VERB', 'ADJF', 'ADJS', 'INFN', 'PRTF', 'PRTS', 'GRND'}:
            if not ('Name' in word_max.tag or
                    'Surn' in word_max.tag or
                    'Patr' in word_max.tag or
                    'Abbr' in word_max.tag or
                    'Geox' in word_max.tag or
                    'Apro' in word_max.tag or
                    'LATN' in word_max.tag or
                    'PNCT' in word_max.tag or
                    'NUMB' in word_max.tag or
                    'intg' in word_max.tag or
                    'real' in word_max.tag or
                    'ROMN' in word_max.tag or
                    'UNKN' in word_max.tag) and (len(word_max.normal_form) > 3):
                row.append(word_max.normal_form)

    result.append(row)

# Убираем стоп-слова, пунктуацию, нерусские слова и числа
result = [[word
           for word in sentence
           if word not in new_stopwords and
           word not in new_punctuation and not
           re.findall('^[A-Za-z0-9\-\+]*$|^[A-Za-z]*\-[А-Яа-я]*$|^[А-Яа-я]*[0-9]+$', word)
           ] for sentence in result]
print('result =', result)

# Склеиваем обратно в строки
clear_strings = [reduce(lambda a, b: a + ' ' + b, row) for row in result]
# print('clear_strings =', clear_strings)

# Определяем различные токены
vectorizer = TfidfVectorizer(max_features=128)
vectorizer.fit(clear_strings)
for name_ in vectorizer.get_feature_names():
    print(name_)
