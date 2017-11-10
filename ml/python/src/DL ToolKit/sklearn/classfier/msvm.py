#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:SVM分类预测
	Ref:
	Date:2017年8月26日
	Author:tuling56
'''

from sklearn import svm
X=[[0,0],[1,1]]
y=[0,1]
clf=svm.SVC()
clf.fit(X,y)
clf.predict([[2.,2.]])