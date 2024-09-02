import jieba
import os
from collections import Counter, defaultdict
import numpy as np
import re
import dill


class Posting(object):
    special_doc_id = -1
    def __init__(self, docid, tf=0):
        self.docid = docid
        self.tf = tf
    def __repr__(self):
        return "<docid: %d, tf: %d>" % (self.docid, self.tf)

def invert_batch(batch):
    count = 0
    for file in batch:
        filepath = os.path.join('final_txt', file)
        docid = re.split(r'[_\\.]+', filepath)[-3]
        filename = os.path.splitext(file)[-1]
        with open(filepath, 'r', encoding='utf-8') as fin:
            content = fin.readlines()[1:]
            contents = " ".join(line.strip() for line in content)
            terms = [term for term in jieba.cut(contents) if (len(term.strip()) > 1) and (term not in stop_list)]
            if terms == [] or terms == None:
                terms = ['空文件']
            for term in terms:
                term_docid_pairs.append((term, docid))
            # for term in jieba.cut(contents):
                # if (len(term.strip()) <= 1) or (term in stop_list):
                    # continue
            term_counts = np.array(list(Counter(terms).values()))
            log_func = np.vectorize(lambda x: 1.0 + np.log10(x) if x > 0 else 0.0)
            log_tf = log_func(term_counts)
            count += 1
            print(f'term_counts {count}//250 logged')
            
            doc_length.append((docid, np.sqrt(np.sum(log_tf**2))))

    

jieba.load_userdict('jieba_dict.txt')
stop_list = []
with open('baidu_stopwords.txt', 'r', encoding='utf-8') as stop_f:
    for item in stop_f.readlines():
        stop_list.append(item.rstrip())


term_docid_pairs = []
doc_length = []

batch_size = 250
count = 0
batch = []
batch_num = 33
for file in os.listdir('final_txt'):
    batch.append(file)
    if len(batch) == batch_size:
        count += 1
        invert_batch(batch)
        batch = []
        print(f'Batch ({count}/33) has been inverted.')

term_docid_pairs = sorted(term_docid_pairs)
doc_length = sorted(doc_length, key=lambda x: x[0])

inverted_index = defaultdict(lambda: [Posting(Posting.special_doc_id, 0)])

for term, docid in term_docid_pairs:
    postings_list = inverted_index[term]
    if docid != postings_list[-1].docid:
        postings_list.append(Posting(docid, 1))
    else:
        postings_list[-1].tf += 1


fout1 = open('doc_length.pkl', 'wb')
dill.dump(doc_length, fout1)
fout1.close()
fout2 = open('inverted_index.pkl', 'wb')
dill.dump(inverted_index, fout2)
fout2.close()
    
