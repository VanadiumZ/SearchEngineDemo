def evaluate(query: str) -> list:
    '''
    各位同学需要完成evaluate函数，通过调用之前自己的代码来实现搜索引擎的功能
    参数：query，字符串类型，它代表查询
    返回值：url_list，它是一个长为20的url列表
    '''

    from collections import defaultdict, Counter
    import jieba
    import numpy as np
    import dill
    import os

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
    from query import retrieval_url

    url_list = retrieval_url(query)


    return url_list
    