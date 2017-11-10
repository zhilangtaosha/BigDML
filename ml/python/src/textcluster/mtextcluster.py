#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：文本聚类程序演示
      参考：http://python.jobbole.com/85481/
'''

import numpy as np
import pandas as pd
import nltk
import re
import os,sys
import codecs
from sklearn import feature_extraction
import mpld3
from bs4 import  BeautifulSoup


data_dir='../../data/text_cluster'

'''
    功能函数
'''
# 分词并词干化
# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed
from nltk.stem.snowball import SnowballStemmer
def tokenize_and_stem(text):
    # load nltk's SnowballStemmer as variabled 'stemmer'
    stemmer = SnowballStemmer("english")
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

# 分词
def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

#tfidf化
from  sklearn.feature_extraction.text import TfidfVectorizer
def tfidf(synopses):
    tfidf_vectorizer=TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.2, stop_words='english', use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(synopses)
    print(tfidf_matrix.shape)
    terms=tfidf_vectorizer.get_feature_names()
    print terms

    return  tfidf_matrix  # 返回tfidf矩阵


'''
    step1:文本预处理:去停用词，分词和词干化
'''
def textProc():
    #import three lists: titles, links and wikipedia synopses
    titles = open(os.path.join(data_dir,'title_list.txt')).read().split('\n')
    #ensures that only the first 100 are read in
    titles = titles[:100]

    # 链接
    links = open(os.path.join(data_dir,'link_list_imdb.txt')).read().split('\n')
    links = links[:100]

    # 类别
    genres = open(os.path.join(data_dir,'genres_list.txt')).read().split('\n')
    genres = genres[:100]

    # 摘要处理（wiki和imdb的合并）
    synopses_wiki = open(os.path.join(data_dir,'synopses_list_wiki.txt')).read().split('\n BREAKS HERE')
    synopses_wiki = synopses_wiki[:100]
    synopses_clean_wiki = []
    for text in synopses_wiki:
        text = BeautifulSoup(text, 'html.parser').getText()
        #strips html formatting and converts to unicode
        synopses_clean_wiki.append(text)
    synopses_wiki = synopses_clean_wiki

    synopses_imdb = open(os.path.join(data_dir,'synopses_list_imdb.txt')).read().split('\n BREAKS HERE')
    synopses_imdb = synopses_imdb[:100]
    synopses_clean_imdb = []
    for text in synopses_imdb:
        text = BeautifulSoup(text, 'html.parser').getText()
        #strips html formatting and converts to unicode
        synopses_clean_imdb.append(text)
    synopses_imdb = synopses_clean_imdb

    synopses = []
    for i in range(len(synopses_wiki)):
        item = synopses_wiki[i] + synopses_imdb[i]
        synopses.append(item)

    # title,links,synopses,genres
    print(str(len(titles)) + ' titles')
    print(str(len(links)) + ' links')
    print(str(len(synopses)) + ' synopses')
    print(str(len(genres)) + ' genres')

    # generates index for each item in the corpora (in this case it's just rank) and I'll use this for scoring later
    ranks = []
    for i in range(0,len(titles)):
        ranks.append(i)

    # 分词，去停用词和词干化
    # load nltk's English stopwords as variable called 'stopwords'
    stopwords = nltk.corpus.stopwords.words('english')

    totalvocab_stemmed = []
    totalvocab_tokenized = []
    for i in synopses:
        allwords_stemmed = tokenize_and_stem(i)
        totalvocab_stemmed.extend(allwords_stemmed)

        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)

    # 去停用词
    # 暂时未操作

    # 构造原始材料
    vocab_frame=pd.DataFrame({'words':totalvocab_tokenized},index=totalvocab_stemmed)
    print(vocab_frame)



'''
    step2:计算文本余弦相似度
'''
from sklearn.metrics.pairwise import cosine_similarity
def calcSimilarty(tfidf_matrix):
    dist=1-cosine_similarity(tfidf_matrix)
    print dist


'''
    step3:K-means文本聚类
'''
from sklearn.cluster import KMeans
def textCluster(tfidf_matrix):
    num_cluster=5
    km=KMeans(n_clusters=num_cluster)
    km.fit(tfidf_matrix)
    clusters=km.labels_.tolist()

    # 评估阶段
    films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters, 'genre': genres }
    frame = pd.DataFrame(films, index = [clusters] , columns = ['rank', 'title', 'cluster', 'genre'])

#也可以将分类器保存下来
from sklearn.externals import joblib
def textClusterLoad():
    km=joblib.load('doc_cluster.pkl')
    clusters=km.labels_.tolist()



'''
   step4: 聚类可视化
'''
def cluster_visual():
    pass

def clusterVisual():
    pass


if __name__ == "__main__":
    textProc()
