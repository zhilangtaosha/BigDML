#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:scikit-learn解多元线性回归
    Ref:http://www.shareditor.com/blogshow/?blogId=54
    State：
    Date:2017/2/10
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

'''
    设计二元一次方程：y=1+2x1+3x2
    取样本为(1,1,1),(1,1,2),(1,2,1)，计算得y=(6,9,8)
    注意：这里面常数项1相当于1*x0，只不过这里的x0永远取1

    所以我们的
    X = [[1,1,1],[1,1,2],[1,2,1]]   #三元线性方程组
    y = [[6],[9],[8]]

    问题的关键在于给出X,和y的一组解
'''



from numpy.linalg import  inv
from numpy import  dot, transpose

from numpy.linalg import lstsq

from sklearn.linear_model import LinearRegression


#多元线性回归问题求解
def muti_regress():
    X = [[1,1,1],[1,1,2],[1,2,1]]
    y = [[6],[9],[8]]

    #用矩阵运算的方式
    print dot(inv(dot(transpose(X),X)), dot(transpose(X),y))

    #用最小二乘法
    print lstsq(X, y)[0]

    #用scikit-learn的线性回归模型
    model = LinearRegression()
    model.fit(X, y)
    x2 = [[1,3,5]]
    y2 = model.predict(x2)
    print y2


if __name__ == "__main__":
    muti_regress()

