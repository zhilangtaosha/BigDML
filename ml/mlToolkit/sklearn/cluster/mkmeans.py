#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun: k-means聚类演示
	Ref:http://www.shareditor.com/blogshow/?blogId=61
	Date:2016/9/5
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import matplotlib.pyplot as plt
import numpy as np


'''
	生成聚类数据
'''
X=[]
Xc=[]
def generate_data():
	global X,Xc
	############生成类别明显的数据
	# 生成2*10的矩阵，且值均匀分布的随机数
	cluster1 = np.random.uniform(0.5, 1.5, (2, 10))
	cluster2 = np.random.uniform(3.5, 4.5, (2, 10))

	# 顺序连接两个矩阵，形成一个新矩阵,所以生成了一个2*20的矩阵，T做转置后变成20*2的矩阵,刚好是一堆(x,y)的坐标点
	X = np.hstack((cluster1, cluster2)).T


	###########生成类别不明显的数据
	# 生成2*10的矩阵，且值均匀分布的随机数
	cluster1 = np.random.uniform(0.5, 1.5, (2, 10))
	cluster2 = np.random.uniform(1.5, 2.5, (2, 10))
	cluster3 = np.random.uniform(1.5, 3.5, (2, 10))
	cluster4 = np.random.uniform(3.5, 4.5, (2, 10))

	# 顺序连接两个矩阵，形成一个新矩阵,所以生成了一个2*20的矩阵，T做转置后变成20*2的矩阵,刚好是一堆(x,y)的坐标点
	X1 = np.hstack((cluster1, cluster2))
	X2 = np.hstack((cluster3, cluster4))
	Xc = np.hstack((X1, X2)).T

	plt.figure()
	plt.axis([0, 5, 0, 5])
	plt.grid(True)

	plt1 = plt.subplot(2,1,1)
	plt1.plot(X[:,0],X[:,1],'k.')

	plt2=plt.subplot(2,1,2)
	plt2.plot(Xc[:,0],Xc[:,1],'k.')

	plt.show()


'''
	指定聚类数目
'''
from sklearn.cluster import KMeans
def mkmeans():
	kmeans = KMeans(n_clusters=2)
	kmeans.fit(X)
	plt.figure()
	plt.plot(X[:,0],X[:,1],'k.')
	plt.plot(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], 'ro')
	plt.show()

'''
	用肘部法则确定聚类数目
'''
from scipy.spatial.distance import cdist
def detemin_clusternum():
	K = range(1, 10)
	meandistortions = []
	for k in K:
		kmeans = KMeans(n_clusters=k)
		kmeans.fit(Xc)
		# 求kmeans的成本函数值
		meandistortions.append(sum(np.min(cdist(Xc, kmeans.cluster_centers_, 'euclidean'), axis=1)) / Xc.shape[0])

	plt.figure()
	plt.grid(True)
	plt.plot(K, meandistortions, 'bx-')
	plt.show()


if __name__ == "__main__":
	generate_data()
	mkmeans()
	detemin_clusternum()

