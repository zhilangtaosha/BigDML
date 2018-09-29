##数据科学笔记
[TOC]

### 基础

#### 统计理论

统计学思考方法的6大特征，p值、置信区间、回归模型等，

> 在使用回归模型的时候假设多个解释变量之间没有相乘效果。

#### 统计指标

##### 相关系数

 皮尔逊相关也称为积差相关（或积矩相关）是英国统计学家皮尔逊于20世纪提出的一种计算直线相关的方法。

1.具体描述如下：

假设有两个变量X、Y，那么两变量间的皮尔逊相关系数可通过以下公式计算：

公式一：

![皮尔逊相关系数计算公式](http://hi.csdn.net/attachment/201007/11/19961_12788382715I69.gif)

公式二：

![皮尔逊相关系数计算公式](http://hi.csdn.net/attachment/201007/11/19961_1278838271Lch3.gif)

公式三：

![皮尔逊相关系数计算公式](http://hi.csdn.net/attachment/201007/11/19961_1278838271OR17.gif)

公式四：

![皮尔逊相关系数计算公式](http://hi.csdn.net/attachment/201007/11/19961_1278843346L5kz.gif)

以上列出的四个公式等价，其中E是数学期望，cov表示协方差，N表示变量取值的个数。

 2、适用范围

 当两个变量的标准差都不为零时，相关系数才有定义，皮尔逊相关系数适用于：

(1)、两个变量之间是线性关系，都是连续数据。

(2)、两个变量的总体是正态分布，或接近正态的单峰分布。

(3)、两个变量的观测值是成对的，每对观测值之间相互独立。

### 实现

所有与语言底层相关的实现都集中放到这里进行处理

#### python

python数据处理三剑客：numpy/pandas/scipy

##### numpy

```python

```

##### pandas

```python

```

##### scipy

```python

```

#### r

DataFrame作为R中的基础数据结构

```R

```

### 专题

#### 命令行数据处理

安装相关工具箱(除linux本身提供的命令外)

##### 准备工作

###### csvkit 

```shell
pip install csvkit
```

提供的命令有

```shell
/usr/bin/csvclean
/usr/bin/csvcut
/usr/bin/csvformat
/usr/bin/csvgrep
/usr/bin/csvjoin
/usr/bin/csvjson
/usr/bin/csvlook
/usr/bin/csvpy
/usr/bin/csvsort
/usr/bin/csvsql
/usr/bin/csvstack
/usr/bin/csvstat
/usr/bin/in2csv
/usr/bin/sql2csv
```

###### csvtotable

```shell
pip install csvtotable
```

提供的命令有：

```shell
/usr/bin/csvtotable
```

###### jq

```shell

```

###### q

```shell

```

##### Obtaining Data

```shell
sql2csv --db 'mysql://root:root@localhost/test' --query 'select * from orders'
```

##### Scrubbing Data

```shell

```

##### Exploring Data

```shell

```

##### Modeling Data

```shell

```

##### Interpreting Data

```shell

```

#### 海量数据处理

//这个必须作为一个专题来讲，参考面试之法，编程之道部分

##### 排序

##### 查找

1亿条记录数据(有重复)，查找出现最多的10条

 ##参考

- **基础**

  [相关系数](http://m.blog.csdn.net/ciedecem/article/details/39582635)

  [数据科学完整学习路径-Python版（推荐）](https://www.tuicool.com/articles/QBZzquY)

- **专题**

  [DataScienceAttheCommandLine](https://github.com/jeroenjanssens/data-science-at-the-command-line)


