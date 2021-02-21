from sklearn.feature_extraction.text import TfidfVectorizer

documents = ['I like this movie, it\'s funny.',
           'I hate this movie.',
           'This was awesome! ',
           'I like it.Nice one. ',
           'I love it.']

tfidf_vectorizer = TfidfVectorizer()
values = tfidf_vectorizer.fit_transform(documents)

feature_names = tfidf_vectorizer.get_feature_names()

# print(feature_names)
# print(values.toarray())
