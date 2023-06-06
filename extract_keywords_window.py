import os.path
import re
import sys

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def pre_process(text):
    return re.sub(r"(\d|\W)+", " ", text)


def get_stop_words(path):
    with open(path, encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


stopwords = get_stop_words(
    r"C:\!Drv\WinPython-32bit-3.4.4.2Qt5\python-3.4.4"
    r"\Lib\site-packages\wordcloud\stopwords"
)

with open(sys.argv[-2], "rb") as f:
    data = f.read()
    text = pre_process(data.decode("utf-8", "replace"))

n_docs = int(sys.argv[-1])
docs = []
start = 0
for i in range(n_docs):
    end = start + len(text) // n_docs
    end = end + re.search(r"\s|$", text[end:]).span()[0]
    docs.append(text[start:end])
    start = end

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
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]
    return results


def kwords(doc):
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)
    return keywords


a = [
    sorted(list(kwords(doc).items()), key=lambda x: x[1], reverse=True) for doc in docs
]
print(a[0])
names = ["{:03d}".format(i) for i in range(len(a))]
d = pd.DataFrame(
    [[y[0] for y in x] for x in a], index=[os.path.basename(name) for name in names]
)
d.to_csv("keywords.csv")
