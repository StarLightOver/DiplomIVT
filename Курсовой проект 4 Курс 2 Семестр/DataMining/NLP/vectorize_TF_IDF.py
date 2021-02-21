# -------------------------------------------------
# Здесь собирается частотный словарь для дальнейшего анализа методом TF-IDF
# -------------------------------------------------

from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity
from NLP.CSVmodule import *
from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2
import nltk
from functools import reduce
import re
from NLP.read_write import *
import pickle


class TextToVectorTfIdf:
    """
    Функция инициализации класса по векторизации текста
    """

    def __init__(self):
        # Загружаем словарь стоп слов и добавляем к ним доколнительные
        self.__download_stopwords(['из-за', 'который', 'около'])
        # Загружаем пунктуацию и добавляем дополнительные
        self.__punctuation = [pun for pun in punctuation] + ["''", '``', '–']
        # Модель tf-idf
        self.__vectorizer_tfidf = None
        # Словарь, если вдруг захочется посмотреть...
        self.vocabulary = None

    """
    Функция загрузки стоп-слов
    
    Параметры
    ----------
    dop_words : [] - массив дополнительных стоп-слов, которых нет в загружаемом словаре
    """

    def __download_stopwords(self, dop_words: []):
        try:
            self.__stopwords = nltk.corpus.stopwords.words('russian')
        except TypeError:
            nltk.download('stopwords')
            self.__stopwords = nltk.corpus.stopwords.words('russian')
        finally:
            self.__stopwords += dop_words

    """
    Функция загрузки необработанных данных

    Параметры
    ----------
    filename: str = 'data_society_2020.csv' - csv таблица, хранящая строки данных
    """

    def load_data(self, filename: str = 'data_society_2020.csv'):
        # Считываем данные из датасета
        data = csv_reader(filename)

        # Выбираем заголовки статей
        text = [dat[3] for dat in data]

        # Предварительная обработка текста
        self.__prepare_data(text)

    """
    Секретная функция для обработки

    Параметры
    ----------
    words: [] - массив
    """

    def __max_score(self, some_words: []):
        value_max = some_words[0].score
        index_max = 0

        for i in range(1, len(some_words)):
            if some_words[i].score > value_max:
                value_max = some_words[i].score
                index_max = i

        return index_max

    """
    Функция предварительной обработки данных

    Параметры
    ----------
    text: [] - массив строк
    """

    def __prepare_data(self, text: []):
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
                word_max = temp[self.__max_score(temp)]
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
                   if word not in self.__stopwords and
                   word not in self.__punctuation and
                   not re.findall('^[A-Za-z0-9\-\+]*$|^[A-Za-z]*\-[А-Яа-я]*$|^[А-Яа-я]*[0-9]+$', word)
                   ] for sentence in result]

        # Склеиваем обратно в строки
        new_result = []
        for row in result:
            if len(row) == 0:
                new_result.append('')
            elif len(row) == 1:
                new_result.append(row[0])
            else:
                new_result.append(reduce(lambda a, b: a + ' ' + b, row))
        self.clear_strings = new_result
        # self.clear_strings = [reduce(lambda a, b: a + ' ' + b, row) if len(row) != 0 else '' for row in result]

    """
    Функция обучающая модель

    Параметры
    ----------
    max_features=None - Если не None, при создании словаря учитывает только верхние max_features, 
                        упорядоченные по частоте термина по всему корпусу.
    filename=None - название файла
    """

    def train_model(self, max_features=None, filename=None):
        # Если данные для обработки не были загружены, вывести ошибку
        if 'clear_strings' not in self.__dir__():
            print('Ошибка: Данные не были загружены! Используйте load_data()')
            return None

        self.__vectorizer_tfidf = TfidfVectorizer(max_features=max_features)

        self.__vectorizer_tfidf.fit(self.clear_strings)

        write_mas('vocabulary.txt', self.__vectorizer_tfidf.get_feature_names())

        if filename is not None:
            # TODO Супер-мега проверка на то, что файл существет
            # Сохранить модель
            self.__save_model(self.__vectorizer_tfidf, filename)

    """
    Функция сохранить модель

    Параметры
    ----------
    data - что нужно сохранить
    filename - название файла
    """

    def __save_model(self, data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    """
    Функция зашрузить модель

    Параметры
    ----------
    filename - название файла
    """

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.__vectorizer_tfidf = pickle.load(f)

    """
    Функция для обработки строки

    Параметры
    ----------
    text: str - строка
    
    Вернуть
    ----------
    csr_matrix - сложно описать, лучше загуглить...
    """

    def get_vector(self, text: str):
        # Обработать текст
        self.__prepare_data([text])
        # Вернуть вектор
        return self.__vectorizer_tfidf.transform([text])


if __name__ == "__main__":
    temp = TextToVectorTfIdf()
    temp.load_data()
    temp.train_model(filename='vectorizer_tfidf.pickle', max_features=512)
    vector = temp.get_vector('Адвокат депутат любит коронавирус и Москву. Он хочет туда вернутся.')
    print(vector)
    print('------------------------------')
    vector2 = temp.get_vector('Адвокат в августе взял в Москву короновирус и акуловый арендатор хочет вернутся туда')
    print(vector2)
    print('------------------------------')
    print(cosine_similarity(vector.toarray(), vector2.toarray()))

    temp2 = TextToVectorTfIdf()
    temp2.load_model('vectorizer_tfidf.pickle')
    vector = temp.get_vector('Адвокат любит коронавирус и Москву. Он хочет туда вернутся.')
    print(vector)
    print('------------------------------')
    vector2 = temp.get_vector('Адвокат в августе взял в Москву короновирус. Арендатор хочет вернутся туда')
    print(vector2)
    print('------------------------------')
    print(cosine_similarity(vector.toarray(), vector2.toarray()))
