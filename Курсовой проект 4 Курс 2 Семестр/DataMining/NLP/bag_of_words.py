# -------------------------------------------------
# Здесь собирается словарь для дальнейшего анализа методом BOW
# -------------------------------------------------

from string import punctuation
from nltk.corpus import stopwords
from NLP.CSVmodule import *
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2
import nltk
from functools import reduce
import re
from NLP.read_write import *
import numpy as np

# nltk.download('stopwords')
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
result = [[morph.parse(word)[0].normal_form for word in sentence] for sentence in words]

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
print('clear_strings =', clear_strings)

# Определяем различные токены
vectorizer = CountVectorizer()
bow_vector = vectorizer.fit_transform(clear_strings)
print('count =', len(vectorizer.get_feature_names()), '; names =', vectorizer.get_feature_names())
write_mas('vocabulary.txt', vectorizer.get_feature_names())

data_vectors = [sorted(x.indices.tolist()) for x in bow_vector]
print(data_vectors)

