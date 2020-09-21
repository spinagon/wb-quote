import glob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import re
import os.path
import sys

def pre_process(text):
    return re.sub(r"(\d|\W)+", " ", text)

def get_stop_words(path):
    with open(path, encoding='utf-8') as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

stopwords = get_stop_words(r"C:\!Drv\WinPython-32bit-3.4.4.2Qt5\python-3.4.4\Lib\site-packages\wordcloud\stopwords")

work = sys.argv[-1]

names = glob.glob(work + '/*.txt')
docs = []
for name in names:
    with open(name, encoding='utf-8') as f:
        docs.append(pre_process(f.read()))

cv = CountVectorizer(max_df=0.85, stop_words=stopwords, max_features=10000)
word_count_vector = cv.fit_transform(docs)
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)
feature_names = cv.get_feature_names()
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []
    for idx, score in sorted_items:
        fname = feature_names[idx]
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    return results

def kwords(doc):
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)
    return keywords

a = [
    sorted(list(kwords(doc).items()), key=lambda x: x[1], reverse=True)
    for doc in docs]
print(a[0])
d = pd.DataFrame(
    [[y[0] for y in x] for x in a],
    index=[os.path.basename(name) for name in names])
d.to_csv(work + '/keywords.csv')
