#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：scilit-learn步步实践
  参考：http://kukuruku.co/hub/python/introduction-to-machine-learning-with-python-andscikit-learn
'''

'''
    数据预处理
'''
import  numpy as np
import  urllib

# 数据加载和预处理
from sklearn import preprocessing
def loaddata():
    url="http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
    raw_data=urllib.urlopen(url)
    dataset=np.loadtxt(raw_data,delimiter=',')
    X=dataset[:,0:8]
    y=dataset[:,8]
    # data normalization
    norm_X=preprocessing.normalize(X)
    stand_X=preprocessing.scale(X)
    return  X,y

'''
    特征工程
'''
# 特征选择1（利用Tree算法算出特征的重要性）
from sklearn.ensemble import ExtraTreesClassifier
def featureselect(X,y):
    modle=ExtraTreesClassifier()
    modle.fit(X,y)
    print(modle.feature_importances_)

# 特征选择2（利用高校的特征子集搜索算法，选出最好的特征子集）
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
def featureselect2(X,y):
    modle=LogisticRegression()
    rfe=RFE(modle,3)  # 选取3个特征属性
    rfe=rfe.fit(X,y)
    print (rfe.support_)
    print (rfe.ranking_)

'''
    分类参数优化
'''
#网格搜索估计
from sklearn.linear_model import Ridge
from sklearn.grid_search import GridSearchCV
def GridOpti():
    #准备测试的一系列参数
    alphas=np.array([1,0.1,0.01,0.001,0.0001,0])
    # 创建和拟合回归模型，测试每个参数的表现
    model=Ridge()
    grid = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
    grid.fit(X, y)
    print(grid)
    #总结网格搜索的结果
    print(grid.best_score_)
    print(grid.best_estimator_)

#随机选择和验证
from scipy.stats import uniform as sp_rand
from sklearn.grid_search import RandomizedSearchCV
def RandTest():
    # prepare a uniform distribution to sample for the alpha parameter
    param_grid = {'alpha': sp_rand()}
    # create and fit a ridge regression model, testing random alpha values
    model = Ridge()
    rsearch = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=100)
    rsearch.fit(X, y)
    print(rsearch)
    # summarize the results of the random parameter search
    print(rsearch.best_score_)
    print(rsearch.best_estimator_.alpha)



'''
    分类算法
'''
# 逻辑斯蒂分类（同时会给出属于该类的概率）
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
def logistic_regress(X,y):
    modle=LogisticRegression()
    modle.fit(X,y)
    print(modle)
    # 做分类决策
    expected=y
    predicted=modle.predict(X)
    # 总结分类结果
    print(metrics.classification_report(expected,predicted))
    print(metrics.confusion_matrix(expected,predicted))

# 贝叶斯分类（同时会给出属于该类的概率）
from sklearn.naive_bayes import GaussianNB
def bayes(X,y):
    modle=GaussianNB()
    modle.fit(X,y)
    print(modle)
    # 做分类决策
    expected=y
    predicted=modle.predict(X)
    # 总结分类结果
    print(metrics.classification_report(expected,predicted))
    print(metrics.confusion_matrix(expected,predicted))

# k最近邻分类（同时会给出属于该类的概率）
from sklearn.neighbors import KNeighborsClassifier
def knn(X,y):
    modle=KNeighborsClassifier()
    modle.fit(X,y)
    # 做分类决策
    expected=y
    predicted=modle.predict(X)
    # 总结分类结果
    print(metrics.classification_report(expected,predicted))
    print(metrics.confusion_matrix(expected,predicted))

# 决策树(CART分类和回归树）
from sklearn.tree import DecisionTreeClassifier
def cart(X,y):
    modle=DecisionTreeClassifier()
    modle.fit(X,y)
    # 做分类决策
    expected=y
    predicted=modle.predict(X)
    # 总结分类结果
    print(metrics.classification_report(expected,predicted))
    print(metrics.confusion_matrix(expected,predicted))

# svm分类
from sklearn.svm import SVC
def svm(X,y):
    modle=SVC()
    modle.fit(X,y)
    # 做分类决策
    expected=y
    predicted=modle.predict(X)
    # 总结分类结果
    print(metrics.classification_report(expected,predicted))
    print(metrics.confusion_matrix(expected,predicted))

# 神经网络进行分类
def neuralnetwork(X,y):
    # 目前版本的sklearn还不直接支持神经网络：换用其它的包：http://www.zhihu.com/question/24738573
    pass


'''
    程序入口
'''
if __name__ == "__main__":
    # 预处理部分
    X,y=loaddata()

    # 特征工程
    #featureselect(X,y)
    #featureselect2(X,y)

    #####参数优化部分
    #GridOpti()
    #RandTest()

    #####(分类)算法部分
    #logistic_regress(X,y)
    #bayes(X,y)
    #knn(X,y)
    #cart(X,y)
    #svm(X,y)
