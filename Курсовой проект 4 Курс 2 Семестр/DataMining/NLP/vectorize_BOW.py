# -------------------------------------------------
# Здесь по известному словарю строится вектор
# Который предстовляет собой набор чисел, соответствующих значащим битам
# -------------------------------------------------

from string import punctuation
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2
import nltk
from functools import reduce
import re
from NLP.read_write import *

# Загружаем стоп-слова + дополнительные
new_stopwords = stopwords.words('russian') + ['из-за', 'который', 'около']

# Загружаем пунктцацию + дополнительные
new_punctuation = [pun for pun in punctuation] + ["''", '``', '–']

# Выбираем заголовки статей
text = 'В августе начинался адвокат, и академик заполнил анкету, арест арест арест'
print('Исходная строка -', text)

# Разбиваем заголовки на токены (слова)
words = nltk.word_tokenize(text)

# Подключаем морфемный анализатор
morph = pymorphy2.MorphAnalyzer()
result = [morph.parse(word)[0].normal_form for word in words]

# Убираем стоп-слова, пунктуацию, нерусские слова и числа
result = [word
          for word in result
          if word not in new_stopwords and
          word not in new_punctuation and not
          re.findall('^[A-Za-z0-9\-\+]*$|^[A-Za-z]*\-[А-Яа-я]*$|^[А-Яа-я]*[0-9]+$', word)]
print('result =', result)

# Склеиваем обратно в строки
clear_string = [reduce(lambda a, b: a + ' ' + b, result)]
print('clear_strings =', clear_string)

data = read_mas('vocabulary.txt')

# Определяем различные токены
vectorizer = CountVectorizer(vocabulary=data)
bow_vector = vectorizer.fit_transform(clear_string)
print('names =', vectorizer.get_feature_names())

data_vectors = sorted(bow_vector.indices.tolist())
print(data_vectors)