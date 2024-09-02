import os
import re
import dill

id_pairs = {}
def get_id_pair(batch):
    count = 0
    for file in batch:
        docid = re.split(r'[_\\.]+', file)[-3]
        id_pairs[docid] = file

batch_size = 250
count = 0
batch = []
batch_num = 33
for file in os.listdir('final_txt'):
    batch.append(file)
    if len(batch) == batch_size:
        count += 1
        get_id_pair(batch)
        batch = []
        print(f'Batch ({count}/33) has been saved.')

id_pairs = dict(sorted(id_pairs.items()))
fout = open('doc_id_pair.pkl', 'wb')
dill.dump(id_pairs, fout)
fout.close()

