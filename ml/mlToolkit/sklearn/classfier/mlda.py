#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:
    Ref: http://scikit-learn.org/0.16/modules/generated/sklearn.lda.LDA.html
    Date:
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

'''
	用lda进行分类（预测）
'''
import numpy as np
from sklearn.lda import LDA
def mlda():
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    y = np.array([1, 1, 1, 2, 2, 2])
    clf = LDA()    #LDA(n_components=None, priors=None, shrinkage=None, solver='svd', store_covariance=False, tol=0.0001)
    clf.fit(X, y)  #训练
    print(clf.predict([[-0.8, -1]]))  #预测


if __name__ == "__main__":
    mlda()

