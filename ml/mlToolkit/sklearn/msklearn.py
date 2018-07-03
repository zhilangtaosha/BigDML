#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：sklearn学习笔记
'''

from sklearn import  datasets
from sklearn import svm
import  numpy as np
import  pylab as pl

'''
    SVM分类演示程序
'''
def msvm_demo():
	X=[[0,0],[1,1]]
	y=[0,1]
	clf=svm.SVC()
	clf.fit(X,y)
	clf.predict([[2.,2.]])


'''
    鸢尾花数据分类
'''
def miris():
    ## 鸢尾花数据
    iris=datasets.load_iris()
    # 数据：包含萼片的铲毒，宽度，花瓣的长度和宽度
    print type(iris.data)
    # 分类：包含每个数据的分类
    print type(iris.target)
    # 分类数据数量化
    print np.unique(iris.target)

    ## 学习和预测（监督学习）
    from sklearn import  svm
    clf=svm.LinearSVC()
    clf.fit(iris.data,iris.target) # 训练得到模型（可以得到模型的各个训练参数）
    print clf.predict([[5.0,3.0,1.2,0.1]])
    print clf.coef_ #获取模型的参数

'''
    利用SVM进行手写数字的识别
    参考：http://toutiao.com/a6327213547014439169/
'''
def handdigit():
    ## 手写数据
    digits=datasets.load_digits()
    #pl.imshow(digits.images[9],cmap=pl.cm.gray_r)
    #pl.show()

    te=digits.images

    ddata = digits.images.reshape(digits.images.shape[0],-1)  #这个展开挺有意思的，可以多学习下
    ddata = digits.images.reshape((len(digits.images), 64))
    print(ddata.shape)



if __name__ == "__main__":
    #miris()
    handdigit()
