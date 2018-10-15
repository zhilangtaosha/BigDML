## 机器学习笔记

[TOC]

### 基础

#### 概念

##### 相似性度量

相似性分析机器学习中的基本概念，是分类聚类等应用的基础，要好好掌握

##### 向量相似性

含文本，矩阵等

```
# 相似矩阵
若A,B都是N阶方阵，若存在可逆矩阵P，使得P(-1)AP=B,则成B是A的相似矩阵，记为A~B
# 相似变换
对A进行P(-1)AP的运算称为对A进行相似变换
```

##### 图片相似性

其本质也是矩阵的相似性，但在处理的时候有所偏重，例如偏重于图像的轮廓描述，就会采用先计算图像轮廓，然后再比较两个轮廓对应的HU距的方式来衡量

### 算法

涵盖经典算法和深度学习算法

#### 经典算法

##### KNN

##### K-means

##### 朴素贝叶斯

##### 逻辑斯蒂回归

##### 决策树

##### 随机深林

##### SVM

#### 深度算法

### 应用

#### 分类

#### 聚类

#### 回归

###### 线性回归

做预测的时候使用到

#### 预测

待补充

### 深度

深度学习框架部分参考mltoolkit，涵盖tensorflow等

## 参考

- **基础**

  [相似矩阵](http://dec3.jlu.edu.cn/webcourse/t000022/teach/chapter5/5_3.htm)

  [机器学习中的相似性度量](http://www.cnblogs.com/chaosimple/archive/2013/06/28/3160839.html)

  [漫谈：机器学习中距离和相似性度量方法](http://www.tuicool.com/articles/JJfMBfV)

  [机器学习算法详解系列](http://blog.csdn.net/suipingsp/article/category/2749113)  , [书附代码](https://github.com/Aidan-zhang?utf8=%E2%9C%93&tab=repositories&q=&type=&language=python)（推荐）

  [AndrewNg机器学习教程（Matlab版）](http://openclassroom.stanford.edu/MainFolder/CoursePage.php?course=DeepLearning)

- **算法**

  [数据挖掘的第一步就是搞懂聚类分析](https://www.toutiao.com/i6610682397983769095/)

- **应用**

- **深度**

  ​







