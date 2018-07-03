#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：sklearn学习笔记
'''

from sklearn import  datasets
import  numpy as np
import  pylab as pl

def miris():
    ## 鸢尾花数据
    iris=datasets.load_iris()
    # 数据：包含萼片的铲毒，宽度，花瓣的长度和宽度
    print type(iris.data)
    # 分类：包含每个数据的分类
    print type(iris.target)
    # 分类数据数量化
    print np.unique(iris.target)

    ## 手写数据
    digits=datasets.load_digits()
    #pl.imshow(digits.images[1111],cmap=pl.cm.gray_r)
    #pl.show()
    ddata=digits.images.reshape(digits.images.shape[0],-1)
    print(ddata.shape)

    ## 学习和预测（监督学习）
    from sklearn import  svm
    clf=svm.LinearSVC()
    clf.fit(iris.data,iris.target) # 训练得到模型（可以得到模型的各个训练参数）
    print clf.predict([[5.0,3.0,1.2,0.1]])
    print clf.coef_ #获取模型的参数

    ## 分类
    # k最近邻,svm,线性分类器，逻辑斯蒂

    ## 聚类
    # k 均值聚类

    ## 降维





if __name__ == "__main__":
    miris()
