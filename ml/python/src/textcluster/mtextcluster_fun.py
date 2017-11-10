#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import  print_function
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

num_cluster=5
cluster_colors={0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}
cluster_names = {0: 'Family, home, war',
                 1: 'Police, killed, murders',
                 2: 'Father, New York, brothers',
                 3: 'Dance, singing, love',
                 4: 'Killed, soldiers, captain'}  # 注意这里的每一类选出的词由上一步的聚类结果产生
# 去停用词
# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')

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
    terms=tfidf_vectorizer.get_feature_names()
    print("terms:",terms)
    print(tfidf_matrix.shape)
    return  terms,tfidf_matrix  # 返回tfidf矩阵

'''
    计算文本余弦相似度
'''
from sklearn.metrics.pairwise import cosine_similarity
def calcSimilarty(tfidf_matrix):
    dist=1-cosine_similarity(tfidf_matrix)
    print(dist)
    return  dist


'''
    K-means文本聚类
'''
from sklearn.cluster import KMeans
def textCluster(tfidf_matrix):
    km=KMeans(n_clusters=num_cluster)
    km.fit(tfidf_matrix)
    clusters=km.labels_.tolist()
    print(clusters)
    return  km,clusters


#也可以将分类器保存下来
from sklearn.externals import joblib
def textClusterLoad():
    km=joblib.load('doc_cluster.pkl')
    clusters=km.labels_.tolist()



#层次聚类
from scipy.cluster.hierarchy import ward, dendrogram
def hierarchyCluster(dist,titles):
    linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances
    fig, ax = plt.subplots(figsize=(15, 20)) # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=titles);

    plt.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='major',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='on')

    plt.tight_layout() #show plot with tight layout
    plt.show()
    #uncomment below to save figure
    #plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters

#多尺度分析
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
def mdscaling(dist):
    mds=MDS(n_components=2,dissimilarity="precomputed",random_state=1)
    pos=mds.fit_transform(dist) #降维
    xs,ys=pos[:,0],pos[:,1]
    print()
    return xs,ys

# 主题分析

#去专有名词（但由于是基于大小写的，所以会把句首单词去掉）
import string
def strip_proppers(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word.islower()]
    return "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

# 去除文本中所有专有名词（NNP）和复数名词（NNPS）
from nltk.tag import pos_tag
def strip_proppers_POS(text):
    tagged = pos_tag(text.split()) # 使用 NLTK 的词性标注器
    non_propernouns = [word for word,pos in tagged if pos != 'NNP' and pos != 'NNPS']
    return non_propernouns

# 分词，去专有名词，去停用词完整流程
from gensim import corpora, models, similarities 
def wordfilter(synopses):        
    #remove proper names
    preprocess = [strip_proppers(doc) for doc in synopses]
    #tokenize
    tokenized_text = [tokenize_and_stem(text) for text in preprocess]
    #remove stop words
    texts = [[word for word in text if word not in stopwords] for text in tokenized_text]
    
    # 用文本构建 Gensim 字典
    dictionary = corpora.Dictionary(texts)
    # 去除极端的词（和构建 tf-idf 矩阵时用到 min/max df 参数时很像）
    dictionary.filter_extremes(no_below=1, no_above=0.8)
    # 将字典转化为词典模型（bag of words）作为参考
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda = models.LdaModel(corpus, num_topics=5,
                            id2word=dictionary, 
                            update_every=5, 
                            chunksize=10000, 
                            passes=100)
        
    print(lda.show_topics())

    # 取出前20个词
    topics_matrix = lda.show_topics(formatted=False, num_words=20)
    topics_matrix = np.array(topics_matrix)
    topic_words = topics_matrix[:,:,1]
    for i in topic_words:
        print([str(word) for word in i])


#数据可视化（使用matplotlib和mpld3）
def dataVisualStatic(xs,ys,clusters,titles):
    df=pd.DataFrame(dict(x=xs,y=ys,label=clusters,title=titles))
    print(df.head())
    #group by cluster
    groups = df.groupby('label')
    print(groups)

    #绘图设置
    fig,ax=plt.subplots(figsize=(17,9))
    ax.margins(0.05)
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
                label=cluster_names[name], color=cluster_colors[name],
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params(\
            axis= 'x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off')
        ax.tick_params(\
            axis= 'y',         # changes apply to the y-axis
            which='both',      # both major and minor ticks are affected
            left='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelleft='off')

    ax.legend(numpoints=1)  #show legend with only 1 point

    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)
    plt.show()

# 自定义工具栏（toolbar）位置
class TopToolbar(mpld3.plugins.PluginBase):
    """移动工具栏到分布图顶部的插件"""
    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      this.fig.toolbar.draw();
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}

def dataVisualDynamtic(xs,ys,clusters,titles):
    # 用 MDS 后的结果加上聚类编号和绘色创建 DataFrame
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles))
    # 聚类归类
    groups = df.groupby('label')

    # 自定义 css 对字体格式化以及移除坐标轴标签
    css = """
    text.mpld3-text, div.mpld3-tooltip { font-family:Arial, Helvetica, sans-serif; }
    g.mpld3-xaxis, g.mpld3-yaxis { display: none; }
    svg.mpld3-figure { margin-left: -200px;}
    """

    # 绘图
    fig, ax = plt.subplots(figsize=(14,6)) # 设置大小
    ax.margins(0.03) # 可选项，只添加 5% 的填充（padding）来自动缩放

    # 对聚类进行迭代并分布在绘图,用到了 cluster_name 和 cluster_color 字典的“name”项，这样会返回相应的 color 和 label
    for name, group in groups:
        points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18,label=cluster_names[name], mec='none', color=cluster_colors[name])
        ax.set_aspect('auto')
        labels = [i for i in group.title]

        # 用点来设置气泡消息，标签以及已经定义的“css”
        tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels, voffset=10, hoffset=10, css=css)
        # 将气泡消息与散点图联系起来
        mpld3.plugins.connect(fig, tooltip, TopToolbar())

        # 隐藏刻度线（tick marks）
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])

        # 隐藏坐标轴
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    ax.legend(numpoints=1) # 图例中每项只显示一个点
    mpld3.display()

    # 以下注释语句可以输出 html
    #html = mpld3.fig_to_html(fig)
    #print(html)


####################################主执行流程############################
#import three lists: titles, links and wikipedia synopses
titles = open('data/title_list.txt').read().split('\n')
#ensures that only the first 100 are read in
titles = titles[:100]

# 链接
links = open('data/link_list_imdb.txt').read().split('\n')
links = links[:100]

# 类别
genres = open('data/genres_list.txt').read().split('\n')
genres = genres[:100]

# 摘要处理（wiki和imdb的合并）
synopses_wiki = open('data/synopses_list_wiki.txt').read().split('\n BREAKS HERE')
synopses_wiki = synopses_wiki[:100]
synopses_clean_wiki = []
for text in synopses_wiki:
    text = BeautifulSoup(text, 'html.parser').getText()
    #strips html formatting and converts to unicode
    synopses_clean_wiki.append(text)
synopses_wiki = synopses_clean_wiki

synopses_imdb = open('data/synopses_list_imdb.txt').read().split('\n BREAKS HERE')
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

print("LDA主题模型分析")
wordfilter(synopses) # LDA主题模型分析
sys.exit()

# title,links,synopses,genres
print(str(len(titles)) + ' titles')
print(str(len(links)) + ' links')
print(str(len(synopses)) + ' synopses')
print(str(len(genres)) + ' genres')

# generates index for each item in the corpora (in this case it's just rank) and I'll use this for scoring later
ranks = []
for i in range(0,len(titles)):
    ranks.append(i)

totalvocab_stemmed = []   # 分词并词干化
totalvocab_tokenized = [] # 只分词
for i in synopses:
    allwords_stemmed = tokenize_and_stem(i)
    totalvocab_stemmed.extend(allwords_stemmed)
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)


# 构造原始材料
vocab_frame=pd.DataFrame({'words':totalvocab_tokenized},index=totalvocab_stemmed)
print(vocab_frame)  # 词干和原始词对应pd

# tfidf化
terms,tfidf_matrix=tfidf(synopses)

# 余弦距离
dist=1 - cosine_similarity(tfidf_matrix)

# 开始聚类
km,clusters=textCluster(tfidf_matrix)
print(clusters)

# 聚类分析
films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters, 'genre': genres }
frame = pd.DataFrame(films, index = [clusters] , columns = ['rank', 'title', 'cluster', 'genre'])
frame['cluster'].value_counts() # 聚成的每个类的数目

groupd=frame['rank'].groupby(frame['cluster'])  #每个类中的排名均值，均值越小代表该类的排名越靠前
print(groupd)
print(groupd.mean())

#总结中每个类中最能代表该类的6个词（离聚类中心最近的6个词）
print ("Top terms per cluster:")
order_centroids=km.cluster_centers_.argsort()[:,::-1]
for i in range(num_cluster):
    print("Cluster %d words:" % i,end='')  # replace 6 words per cluster
    for ind in order_centroids[i,:6]:
        print('%s' %vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print()
    print("Cluster %d titles:" % i, end='') # 属于该类的影片
    for title in frame.ix[i]['title'].values.tolist():
         continue
         # print(' %s,' % title, end='')
    print()

# 降维
#xs,ys=mdscaling(dist)  #将每个样本降维到平面上的一个点

# 数据可视化（静态）
#dataVisualStatic(xs,ys,clusters,titles)

#数据可视化（动态交互）
#dataVisualDynamtic(xs,ys,clusters,titles)

#层次聚类
hierarchyCluster(dist,titles)

# 测试入口
if __name__ == "__main__":
    pass
