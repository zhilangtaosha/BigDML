#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:逻辑回归做二分类问题
	Ref: http://www.shareditor.com/blogshow/?blogId=93
	Date:2016/9/5
	Author:tuling56
'''
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression

def mlogistic():
	X = []

	# 前三行作为输入样本
	X.append("fuck you")
	X.append("fuck you all")
	X.append("hello everyone")

	# 后两句作为测试样本
	X.append("fuck me")
	X.append("hello boy")

	# y为样本标注
	y = [1,1,0]

	vectorizer = TfidfVectorizer()

	# 取X的前三句作为输入做tfidf转换
	X_train = vectorizer.fit_transform(X[:-2])
	print X_train
	# 取X的后两句用“上句生成”的tfidf做转换
	X_test = vectorizer.transform(X[-2:])
	print X_test

	# 用逻辑回归模型做训练
	classifier = LogisticRegression()
	classifier.fit(X_train, y)

	# 做测试样例的预测
	predictions = classifier.predict(X_test)
	print predictions



if __name__ == "__main__":
    mlogistic()

