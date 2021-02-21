from NLP.CSVmodule import *
import pymorphy2
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from functools import reduce

# Считываем данные
data = csv_reader('data_society_2020.csv')

# Берем одно предложение
# sentence = data[0][3]
sentence = [dat[3] for dat in data]
# print(sentence)

# Разбиваем на токены
# words = nltk.word_tokenize(sentence)
words = [nltk.word_tokenize(text) for text in sentence]
print(words)

morph = pymorphy2.MorphAnalyzer()
res = [[morph.parse(i)[0].normal_form for i in row] for row in words]
to_str = [reduce(lambda a,b: a + ' ' + b, row) for row in res]
print(to_str)

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(to_str)

print(vectorizer.get_feature_names())
print(len(vectorizer.get_feature_names()))
# for i in X.toarray():
#     print(i)

# Работаем с биграммами
# vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(2, 2))
# X2 = vectorizer2.fit_transform([sentence])
# print(vectorizer2.get_feature_names())
# print(X2.toarray())