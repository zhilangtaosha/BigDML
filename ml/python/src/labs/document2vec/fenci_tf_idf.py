#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Date:
    Author:tuling56
    来自：http://www.2cto.com/kf/201407/317750.html
    功能：jieba实现文档分词和scikit-learn实现文档TF-IDF化
'''

import os
import sys
import re
#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf8')

import jieba
import jieba.posseg as pseg
import string

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

###### 全局变量定义
sFilePath = ".\\segfile\\"   # 分词结果保存目录
tfidfpath = '.\\tfidf'   #tf-idf处理的保存目录


#获取目录下的所有文档(全路径)
def getfiles(datapath):
    filelist=[]
    for root, dirs, files in os.walk(datapath):
        for file in files:
            readfile= os.path.join(root, file)
            filelist.append(readfile)
    return  filelist


'''
    step1:对原始文档进行分词处理
'''
def fenci(filelist) :
    if len(filelist)==0:
        return  0

    stop_cn=""
    with open('../../fenci/stop_cn_1208.txt','r') as f:
        for line in f:
            stop_cn+=str(line.strip().strip('\n'))

    fenci_list=[]
    result = []
    for ffilename in filelist:
        if not os.path.exists(sFilePath) :
            os.mkdir(sFilePath)

        #读取文档
        f = open(ffilename,'r')
        content = f.read().decode('utf8')
        f.close()

        #对文档进行分词处理，采用默认模式
        print(content.encode('utf8'))
        seg = jieba.cut(content.encode('utf8'),cut_all=True)

        #过滤数字和英文字符等
        pattern=re.compile(r'[0-9a-zA-Z]+')
        seg_list=[w for w in seg if (not re.search(pattern,w) and not re.search(w,stop_cn))]

        #对空格，换行符进行处理
        seg_str ='  '.join(seg_list)
        if (seg_str != '' and seg_str != "\n" and seg_str != "\n\n") :
            result.append(seg_list)

        #将分词后的结果用空格隔开，保存至本地。比如"我来到北京清华大学"，分词结果写入为："我 来到 北京 清华大学"
        filename=os.path.split(ffilename)[1]
        fecifile=os.path.abspath(sFilePath)+"\\"+filename+"_seg.txt"
        f = open(fecifile,"w+")
        f.write(seg_str)
        f.close()

        fenci_list.append(fecifile)

    return  fenci_list


'''
    step2:进行TF-IDF计算(在100份已分词好的文档基础上)
'''
def calctfidf(fenci_list) :
    corpus = []  #存取100份文档的分词结果
    for f_fc in fenci_list:
        f = open(f_fc,'r')
        content = f.read()
        f.close()
        corpus.append(content)

    vectorizer = CountVectorizer()    
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    
    word = vectorizer.get_feature_names() #所有文本的关键字
    weight = tfidf.toarray()              #对应的tfidf矩阵

    if not os.path.exists(tfidfpath) :
        os.mkdir(tfidfpath)
 
    # 这里将每份文档词语的TF-IDF写入tfidffile文件夹中保存
    tfidf_list=[]
    for i in range(len(weight)) :
        print u"Writing all the tf-idf into the",i,u" file into ",tfidfpath+'\\'+string.zfill(i,5)+'.txt',"--------"
        tfidffile=os.path.abspath(tfidfpath)+'\\'+string.zfill(i,5)+'.txt'
        tfidf_list.append(tfidffile)
        f = open(tfidffile,'w')
        for j in range(len(word)) :
            f.write(word[j]+"    "+str(weight[i][j])+"\n")
        f.close()
            
if __name__ == "__main__" : 
    path="E:\\Python\\DPython\\Program\\Python\\Cluster\\k_means_textcluster\\K-Means_Text_Cluster\\sougou_material\\origin\\C000007\\"
    filelist=getfiles(path)
    fenci_list=fenci(filelist)
    calctfidf(fenci_list)


