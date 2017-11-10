# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：利用gensim实现文档检索，给出检索的相关性程度
'''

from gensim import corpora,models,similarities

def calcsim():
    #模拟语料库
    corpus= [[(0, 1.0), (1, 1.0), (2, 1.0)],
             [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
             [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
             [(0, 1.0), (4, 2.0), (7, 1.0)],
             [(3, 1.0), (5, 1.0), (6, 1.0)],
             [(9, 1.0)],
             [(9, 1.0), (10, 1.0)],
             [(9, 1.0), (10, 1.0), (11, 1.0)],
             [(8, 1.0), (10, 1.0), (11, 1.0)]]

    tfidf=models.TfidfModel(corpus) #计算语料库的TF-IDF模型
    query_vec=[(0,1),(4,2)]
    tfidf_query=tfidf[query_vec]    #待查询的文档的tfidf统计

    #相似性检索模型
    index=similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=12)

    sims=index[tfidf[query_vec]] #sims的类型是nupmy.ndarray
    print(sims,type(sims))
    print('----------------')
    print(list(enumerate(sims))) #遍历数组，并加上索引



if __name__ == "__main__":
    calcsim()
