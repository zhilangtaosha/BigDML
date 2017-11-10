#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:多项式回归
    Ref:http://www.shareditor.com/blogshow/?blogId=56
    State：
    Date:2017/2/10
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import matplotlib.pyplot as plt
import numpy as np

X = [[50],[100],[150],[200],[250],[300]]
y = [[150],[200],[250],[280],[310],[330]]

X_test = [[250],[300]] # 用来做最终效果测试
y_test = [[310],[330]] # 用来做最终效果测试

plt.figure()                     # 实例化作图变量
plt.title(u"一元线性回归和一元多项式回归")
plt.xlabel('x')                 # x轴文本
plt.ylabel('y')                 # y轴文本
plt.axis([30, 400, 100,600])
plt.grid(True)                     # 是否绘制网格线

plt.plot(X, y, 'k.')            # 绘制原始数据图


# 多项式回归
from sklearn.linear_model import LinearRegression     # 线性回归
from sklearn.preprocessing import PolynomialFeatures  # 多项式回归
def polynomial_regress():
    '''
        先用线性回归测试下
    '''
    linemodel=LinearRegression()
    linemodel.fit(X,y)
    x2 = [[30], [320]]
    y2 = linemodel.predict(x2)  # 预测值

    ## 绘制模拟点（模拟点在曲线上）
    plt.plot(x2[0],y2[0],'ro')
    plt.plot(x2[1],y2[1],'ro')

    ## 以这两点为基准绘制拟合曲线
    plt.plot(x2, y2, 'g-')

    '''
        利用多项式回归
    '''
    xx = np.linspace(30, 400, 100)                                 # 设计x轴一系列点作为画图的x点集
    quadratic_featurizer = PolynomialFeatures(degree=2)         # 实例化一个二次多项式特征实例
    X_train_quadratic = quadratic_featurizer.fit_transform(X)     # 用二次多项式对样本X值做变换


    regressor_quadratic = LinearRegression()                     # 创建一个线性回归实例
    regressor_quadratic.fit(X_train_quadratic, y)                 # 以多项式变换后的x值为输入，代入线性回归模型做训练

    # 多形式回归的拟合曲线
    xx_quadratic = quadratic_featurizer.transform(xx.reshape(xx.shape[0], 1)) # 把训练好X值的多项式特征实例应用到一系列点上,形成矩阵
    plt.plot(xx, regressor_quadratic.predict(xx_quadratic), 'r-')               # 用训练好的模型作图(能不能得到其预测方程式)


    '''
        效果评估
    '''
    print u"一元线性回归    r-squared", linemodel.score(X_test, y_test)
    X_test_quadratic = quadratic_featurizer.transform(X_test)                # 都要先先创建一个二次多项式特征实例对样本值进行一下变换
    print u"二次回归        r-squared", regressor_quadratic.score(X_test_quadratic, y_test)


    plt.show() # 展示图像





if __name__ == "__main__":
    polynomial_regress()

