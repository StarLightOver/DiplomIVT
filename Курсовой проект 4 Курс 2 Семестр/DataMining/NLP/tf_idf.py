# -------------------------------------------------
# Здесь собирается частотный словарь для дальнейшего анализа методом TF-IDF
# -------------------------------------------------

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

def prepare_data(text):
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

    # Склеиваем обратно в строки
    clear = [reduce(lambda a, b: a + ' ' + b, row) for row in result]

    return clear


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
# print('clear_strings =', clear_strings)

# Определяем различные токены
vectorizer = TfidfVectorizer(max_features=None)
tf_idf_vector = vectorizer.fit_transform(clear_strings)
print('count =', len(vectorizer.get_feature_names()), '; names =', vectorizer.get_feature_names())
print(tf_idf_vector[1])
print(vectorizer.get_feature_names()[1])
print(vectorizer.get_feature_names()[196])
print(vectorizer.get_feature_names()[454])
print(vectorizer.get_feature_names()[386])
print(vectorizer.get_feature_names()[257])
print(vectorizer.get_feature_names()[531])
print(vectorizer.get_feature_names()[521])

# temp = vectorizer.transform(prepare_data(['Собянин попросил москвичей быть осторожными из-за сильного ветра ']))
# print('-------------')
# print('count =', len(vectorizer.get_feature_names()), '; names =', vectorizer.get_feature_names())
# print(temp)
# temp2 = vectorizer.transform(prepare_data(['Адвокат москвичей Собянин  быть осторожными попросил из-за сильного ветра']))
# print('-------========------')
# print('count =', len(vectorizer.get_feature_names()), '; names =', vectorizer.get_feature_names())
# print(temp2)

# print(euclidean(temp.toarray(), temp2.toarray()))
# print(cosine_similarity(temp.toarray(), temp2.toarray()))

write_mas('vocabulary.txt', vectorizer.get_feature_names())



