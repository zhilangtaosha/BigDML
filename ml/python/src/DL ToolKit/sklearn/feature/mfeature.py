#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:（文本）特征提取
	Ref:http://www.shareditor.com/blogshow/?blogId=58
	Date:2016/9/7
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


'''
	分类变量特征提取
'''
from sklearn.feature_extraction import DictVectorizer
def mfactor():
	onehot_encoder = DictVectorizer()
	instances = [{'city': '北京'},{'city': '天津'}, {'city': '上海'}]
	feature_array=onehot_encoder.fit_transform(instances).toarray()
	print(feature_array,feature_array.shape)
	for feature in onehot_encoder.get_feature_names():
		print feature,   #没一行代表一个样本值

'''
	文本变量有无特征特征提取
'''
from sklearn.feature_extraction.text import CountVectorizer
def wordexist():
	corpus = [
        'UNC played Duke in basketball',
        'Duke lost the basketball game' ]
	vectorizer = CountVectorizer()
	print vectorizer.fit_transform(corpus).todense()
	print vectorizer.vocabulary_  #词库表

'''
	文本变量重要性特征提取(tf-idf)
'''
from sklearn.feature_extraction.text import TfidfVectorizer
def wordimportance():
	corpus = [
        'The dog ate a sandwich and I ate a sandwich',
        'The wizard transfigured a sandwich' ]
	vectorizer = TfidfVectorizer(stop_words='english')
	print(vectorizer.fit_transform(corpus).todense())
	print(vectorizer.vocabulary_)


'''
	标准化（归一化）：均值为0，方差为1
'''
from sklearn import preprocessing
import numpy as np
def standard():
	X = np.array([
		[0., 0., 5., 13., 9., 1.],
		[0., 0., 13., 15., 10., 15.],
		[0., 3., 15., 2., 0., 11.]
		])
	standX=preprocessing.scale(X)
	print standX,standX.mean()
	print "均值:",standX.mean(),"\n方差：",standX.var()




if __name__ == "__main__":
	#mfactor()
	#wordexist()
	#wordimportance()
	standard()

