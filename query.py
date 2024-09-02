from collections import defaultdict, Counter
import jieba
import numpy as np
import dill
import os
import math

jieba.load_userdict('jieba_dict.txt')
# load data record
with open('inverted_index.pkl', 'rb') as fin:
    restore_inverted_index = dill.load(fin)

inverted_index = dict(restore_inverted_index)

with open('doc_length.pkl', 'rb') as fin:
    restore_doc_length = dill.load(fin)

doc_length = dict(restore_doc_length)

with open('doc_id_pair.pkl', 'rb') as fin:
    restore_id_pair = dill.load(fin)

id_pair = dict(restore_id_pair)


def get_url(file):
    with open(os.path.join('final_txt', file), 'r', encoding='utf-8') as f:
        url = (f.readlines()[0].split())[-1]
    return url

def get_posting_list(inverted, query_term):
    try:
        return inverted_index[query_term][1:]
    except KeyError:
        return []

def cosine_scores(inverted_index, doc_length, query, k=3):
    scores = defaultdict(lambda: 0.0)
    query_terms = Counter(term for term in jieba.cut(query))
    for q in query_terms:
        log_func = np.vectorize(lambda x: 1.0 + np.log10(x) if x > 0 else 0.0)
        w_tq = log_func(query_terms[q])
        postings_list = get_posting_list(inverted_index, q)
        for posting in postings_list:
            w_td = log_func(posting.tf)
            scores[posting.docid] += w_td * w_tq
    results = [(docid, score / doc_length[docid]) for docid, score in scores.items()]
    results.sort(key=lambda x: -x[1])
    return results[0:k]

doc_lengths = [doclength for doclength in doc_length.values()]
avg_length = sum(doc_lengths) / len(doc_lengths)
N = len(doc_lengths)

def bm25_scores(inverted_index, doc_length, query, N, k=3, k1=1.5, b=0.75):
    scores =defaultdict(lambda: 0.0)
    query_terms =Counter(term for term in jieba.cut(query))

    for q in query_terms:
        postings_list = get_posting_list(inverted_index, q)
        df = len(postings_list)
        idf = math.log(((N - df + 0.5) / (df + 0.5)) + 1)
        for posting in postings_list:
            tf = posting.tf
            docid = posting.docid
            scores[docid] += idf * (
                (tf * (k1 +1)) / (tf + k1 * (1 - b + b * doc_length[docid]  / avg_length))
            )
    results = [(docid, score) for docid, score in scores.items()]
    results.sort(key=lambda x: -x[1])
    return results[0:k]

# def get_mean_score(inverted_index, doc_length, query, N, k=3, k1=1.5, b=0.75):
#     scores = defaultdict(lambda: 0.0)
#     query_terms = Counter(term for term in jieba.cut(query))
#     for q in query_terms:
#         postings_list = get_posting_list(inverted_index, q)
#         df = len(postings_list)
#         log_func = np.vectorize(lambda x: 1.0 + np.log10(x) if x > 0 else 0.0)
#         w_tq = log_func(query_terms[q])
#         idf = math.log(((N - df + 0.5) / (df + 0.5)) + 1)
#         for posting in postings_list:
#             tf = posting.tf
#             docid = posting.docid
#             w_td = log_func(posting.tf)
#             scores[docid] += ((idf * (
#                 (tf * (k1 +1)) / (tf + k1 * (1 - b + b * doc_length[docid]  / avg_length))
#             )) + w_td * w_tq) / 2
#     results = [(docid, score) for docid, score in scores.items()]
#     results.sort(key=lambda x: -x[1])
#     return results[0:k]











def retrieval_by_score(inverted_index, id_pair, query, k=3):
    top_scores = bm25_scores(inverted_index, doc_length, query, N, k=k)
    results = [(id_pair[docid], score) for docid, score in top_scores]
    return results

def retrieval_url(query, k=20):
    if query:
        results = retrieval_by_score(inverted_index, id_pair,query, k=20)
        url_list = [get_url(result[0]) for result in results]
        return url_list
    else:
        return []

