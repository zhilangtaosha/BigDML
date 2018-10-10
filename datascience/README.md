##数据科学笔记
[TOC]

==除数据可视化外的其它知识点都在此单文档中进行处理==

### 理论

#### 假设检验

统计学思考方法的6大特征，p值、置信区间、回归模型等，

> 在使用回归模型的时候假设多个解释变量之间没有相乘效果。

#### 指标

##### 基础指标

计算均值、方差、中位数、标准差使用函数`mean()`、`var()`、`median()`、`sd`(),这些函数在计算的时候可以根据需要使用`na.rm=TRUE`参数控制是否需要移除空值，`trim`选项用来修剪

##### 扩展指标

###### 相关系数

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

#### 方法

##### 去重

结合使用`duplicated`和`uninque`函数

- vector重复值和非重复值的筛选

```r
x <- round(rnorm(20, 10, 5)) 
#重复值(使用unique的原因是重复值可能出现多次)
unique(x[duplicated(x)]) 
#非重复值
x[!duplicated(x)]
```

- dataframe和matrix重复值和非重复值的筛选

```r
#dataframe重复的判断标准是以行为基准的
df <- read.table(header=T, text=' 
label value 
A 4 
B 3 
C 6 
B 3 
B 1 
A 2 
A 4 
A 4 
') 
# 重复值
unique(df[duplicated(df),])
# 非重复值
unique(df) #或者
df[!duplicated(df),]
```

##### 排序

- vector排序
- dataframe和matrix按指定的列排序

##### 分组

### 工具

#### R

• ggplot2 - 数据绘图

• dplyr - 数据清洗

• tidyr/reshape2 - 数据转换

• lubridate - 处理日期时间数据

• stringr - 字符串处理

• forcats - 处理类别变量

• readr - 文件读写

##### dplyr

dplyr包主要包括3个操作：单表操作、两表操作、数据库操作，主要函数如下：

1. 数据筛选-filter函数
2. 子集选取函数-select函数
3. 数据的排序-arrage函数
4. 数据扩展-mutate函数
5. 数据汇总-summarise函数
6. 数据连接-join函数
7. 分类汇总-group by
8. 管道函数
9. 连接MySQL数据库

###### select

```R

```

###### filter

```R

```

###### sort

```R

```

###### mutate

mutate()函数用来添加列，与cbind()和transform()函数类似，但优于transform();

mutate()函数创建一列时候还可以将其作为变量再来创建后面的列，而transmutate()则是仅包括刚刚创建的变量。

```R
# 保留原有的和新建的
mutate(flights,gain = arr_delay - dep_delay,gain_per_hour = gain / (air_time / 60))

# 只保留新建的
transmute(flights,gain = arr_delay - dep_delay,gain_per_hour = gain / (air_time / 60))
```

###### join

数据记之间的交叉并补运算

```R

```

###### group

主要是summary和group_by函数

```R
# 统计
summarise(flights,delay = mean(dep_delay, na.rm = TRUE))

# 分组
length(levels(factor(flights$tailnum)))
df1<-group_by(flights, tailnum);
df2<-summarise(df1,count=n(),dist=mean(distance,na.rm=TRUE),delay=mean(arr_delay,na.rm=TRUE));
```

###### 抽样

```R
sample_n(flights, 10);
sample_frac(flights,0.1)
```

###### 管道

```R
library(hflights)
library(dplyr)

df<-flights %>%
  group_by(tailnum) %>%
  summarise(count=n(),
            dist=mean(distance, na.rm=TRUE),
            delay=mean(arr_delay,na.rm=TRUE)) %>%
  filter(count>=20 & dist<2000)

df

作者：To_2019_1_4
链接：https://www.jianshu.com/p/7de1429a2f47
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
```

参考：[dplyr高效数据整理工具](https://www.jianshu.com/p/7de1429a2f47)

##### 其它

###### table函数

table函数的数据输出，可以看成是一个带名字的数字向量。可以用names()和as.numeric()分别得到名称和频数

```R
> x <- sample(c("a", "b", "c"), 100, replace=TRUE)
> names(table(x))
[1] "a" "b" "c"
> as.numeric(table(x))
[1] 42 25 33
```

以直接把输出结果转化为数据框，as.data.frame()：

```R
> as.data.frame(table(x))
  x Freq
1 a   42
2 b   25
3 c   33
```

接下来可以使用`pie`进行饼图的绘制，但是饼图的百分比没有办法之间显示，或者用labels标签替换后，就只能显示百分比，不能显示原始标签(此问题待解决)

```R
pie(c3$Freq,labels = c3$Var1)
```

利用图例的方式标注

```R
# Create data for the graph.
x <-  c(21, 62, 10,53)
labels <-  c("London","New York","Singapore","Mumbai")

piepercent<- round(100*x/sum(x), 1)

# Give the chart file a name.
png(file = "city_percentage_legends.png")

# Plot the chart.
pie(x, labels=piepercent, main="City pie chart",col=rainbow(length(x)))
legend("topright", c("London","New York","Singapore","Mumbai"), cex=0.8, fill=rainbow(length(x)))

# Save the file.
dev.off()
```
#### Python

python数据处理三剑客numpy/pandas/scipy

##### numpy

参考numpy基础教程，numpy的矩阵运算比较强大，常配合其它包使用，是基础包

```python

```

##### pandas

两种基础的数据结构Series和DataFrame，Series是一维不同质可变长数组，DataFrame是数据真，tibble是新型的数据结构

```python
dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
'''
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-05 -0.424972  0.567020  0.276232 -1.087401
2013-01-06 -0.673690  0.113648 -1.478427  0.524988
'''

# reindex
df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
df1.index=df1.index.map(str.upper)    
```

> 其它例子：
>
> ```python
> df=pd.DataFrame({'a':[1,2,3],'b':[4,5,6],'c':[7,8,9]},columns=['a','b','c'],index=['11','22','33'])
> ```
>
> 

###### Creation

python结构

```python
# 1.字典方式
data1={ 'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
       }
df1 =pd.DataFrame(data,columns=['pop','year','state','noc'],index=list('ABCDE'))
'''
   pop  year   state  noc
A  1.5  2000    Ohio  NaN
B  1.7  2001    Ohio  NaN
C  3.6  2002    Ohio  NaN
D  2.4  2001  Nevada  NaN
E  2.9  2002  Nevada  NaN
'''

# 2.嵌套列表(列表中的每个元素对应一列)
data2=[['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],[2000, 2001, 2002, 2001, 2002], [1.5, 1.7, 3.6, 2.4, 2.9]]
df2=pd.DataFrame(data2,columns=['state','year','pop','add1','add2'])
'''
  state  year   pop    add1    add2
0  Ohio  Ohio  Ohio  Nevada  Nevada
1  2000  2001  2002    2001    2002
2   1.5   1.7   3.6     2.4     2.9
'''


# 3.嵌套字典
data3 = {'Nevada': {2001: 2.4, 2005: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
df3=pd.DataFrame(data3)
'''
      Nevada  Ohio
2000     NaN   1.5
2001     2.4   1.7
2002     NaN   3.6
2005     2.9   NaN
'''
```

numpy结构

```python
# 数据变形
data4=np.arange(6).reshape(2,3)
df4=pd.DataFrame(data4,columns=['col1','col2','col3'],index=['row1','row2'])
```

###### View

查看整体数据概况

```python
# 属性
df.index
df.columns
df.values

# 函数
df.head()/df.tail(3)
df.describe()

# 缺失值
pd.isna(df)
df.fillna(value=5)
df.dropna(how='any'

```

###### Sort

```python
# 轴排序
df.sort_index(axis=1, ascending=False)

# 值排序
df.sort_values(by='B')
```

###### Selection

row

```python
df[0:3]
df['20130102':'20130104']
df.iloc[3]

# 筛选满足条件的行
df[df.A > 0]
```

col

```python
df['A'] 
df.A

# 赋值
df2['E'] = ['one', 'one','two','three','four','three']
```

row&col

```python
df.loc[:,['A','B']]
df.loc['20130102':'20130104',['A','B']]
df.loc['20130102',['A','B']]
df.loc[dates[0],'A']

df.iloc[3:5,0:2]
df.iloc[[1,2,4],[0,2]]
df.iloc[1:3,:]
df.iloc[:,1:3]
df.iloc[1,1]

# 条件
df[df > 0]
df2[df2['E'].isin(['two','four'])]
```

###### Operations

stats

```python
# 四则运算
df.sub(s, axis='index')
```

apply

```python

```

histograming

```python

```

join

```python

```

append

```python

```

grouping

```python

```

reshape

```python

```

pivot

```python

```

###### Plot

```python
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,columns=['A', 'B', 'C', 'D'])
df = df.cumsum()
plt.figure(); df.plot(); plt.legend(loc='best')
```

###### IO

```python
# 从数据导入
# 导出成文件
```

##### scipy

该包主要牵涉到假设检验等统计学知识点

```python

```

##### 其它

#### Julia

julia是新推出的富有活力的统计语言，融合C、Python、R等助于语言特色，是数据科学领域的又一把顶级利器。

```julia

```

##### 积累

//待补充

### 数据清理

#### 数据接入

//读取各种文件、数据库、网络数据的方式参见r基础部分

#### 特殊处理

##### NA处理

缺失的数据量相对数据集的大小来讲比较小，并且为了不偏离分析，忽略少了的样本或许是最后的策略。

在某些情况下，一些快速修复如均值替代或许是不错的办法。对于这种简单的办法，经常会给数据带来偏差。例如，均值代替法对数据的平均值不会产生变化（这是我们所希望的）。但会减小数据的方差，这不是我们所希望的。

而`mice`包通过合理的数据值可以帮我们填充缺失值。这些合理的数据值都是从一个分布中得到的，这个分布是根据缺失数据点的特定情况设计的。

### 数据转换

#### 长宽格式

长宽格式转换又称行列转换，长数据至少有一列是变量的类型，一列是变量的值，ggplot2中处理的大多都是长数据类型，大多模型比如`lm`,`glm`和`gam`等都利用的也都是长数据，处理数据转换主要是两个reshape2包和tidyr包，其对应的函数功能如下:

| reshape2包 | tidyr包  | 功能                             |
| ---------- | -------- | -------------------------------- |
| melt       | gather   | 函数对宽数据进行处理，得到长数据 |
| cast       | spread   | 函数对长数据进行处理，得到宽数据 |
|            | unit     | 列合并                           |
| colsplit   | separate | 列拆分                           |
|            |          |                                  |

例子:

> 宽数据

```
#   ozone   wind  temp
# 1 23.62 11.623 65.55
# 2 29.44 10.267 79.10
# 3 59.12  8.942 83.90
# 4 59.96  8.794 83.97
```

> 长数据

```
#    variable  value
# 1     ozone 23.615
# 2     ozone 29.444
# 3     ozone 59.115
# 4     ozone 59.962
# 5      wind 11.623
# 6      wind 10.267
# 7      wind  8.942
# 8      wind  8.794
# 9      temp 65.548
# 10     temp 79.100
# 11     temp 83.903
# 12     temp 83.968
```

##### reshape2

reshape2 用得比较多的是`melt`和`cast`两个函数。

- `melt`函数对宽数据进行处理，得到长数据；
- `cast`函数对长数据进行处理，得到宽数据；

###### melt

宽格式得到长格式（列转行）

```R
head(airquality)
  ozone solar.r wind temp month day
1    41     190  7.4   67     5   1
2    36     118  8.0   72     5   2
3    12     149 12.6   74     5   3
4    18     313 11.5   62     5   4
5    NA      NA 14.3   56     5   5
6    28      NA 14.9   66     5   6

library(reshape2)
aql <- melt(airquality, id.vars = c("month", "day"),
  			variable.name = "climate_variable",  #　修改分类变量名
  			value.name = "climate_value")		 #　修改数值变量名
head(aql)
```

###### cast

长格式处理成宽格式（行转列）

![](http://upload-images.jianshu.io/upload_images/58036-d3cdd2487970a0a5.png)

```R
aql <- melt(airquality, id.vars = c("month", "day"))

aqw <- dcast(aql, month + day ~ variable)
head(aqw)

aqws <- dcast(aql, month ~ variable, fun.aggregate = mean, na.rm = TRUE)
head(aqws)
```

在dcast的过程长数据变宽数据，可对宽数据使用聚合函数，演示例子如下：

```R
> head(airquality)
  ozone solar.r wind temp month day
1    41     190  7.4   67     5   1
2    36     118  8.0   72     5   2
3    12     149 12.6   74     5   3
4    18     313 11.5   62     5   4
5    NA      NA 14.3   56     5   5
6    28      NA 14.9   66     5   6

# 先列转行（宽格式->长格式）
> aql <- melt(airquality, id.vars = c("month", "day"))
> head(aql)
  month day variable value
1     5   1    ozone    41
2     5   2    ozone    36
3     5   3    ozone    12
4     5   4    ozone    18
5     5   5    ozone    NA
6     5   6    ozone    28

#　再行转列（长格式－>宽格式）
> aqw <- dcast(aql,month+day~variable)
> head(aqw)
  month day ozone solar.r wind temp
1     5   1    41     190  7.4   67
2     5   2    36     118  8.0   72
3     5   3    12     149 12.6   74
4     5   4    18     313 11.5   62
5     5   5    NA      NA 14.3   56
6     5   6    28      NA 14.9   66

# 在行转列的过程中使用聚合函数
> aqwm <- dcast(aql,month~variable)
Aggregation function missing: defaulting to length

> aqwm <- dcast(aql,month~variable,fun.aggregate = mean)
> head(aqwm)
  month ozone  solar.r      wind     temp
1     5    NA       NA 11.622581 65.54839
2     6    NA 190.1667 10.266667 79.10000
3     7    NA 216.4839  8.941935 83.90323
4     8    NA       NA  8.793548 83.96774
5     9    NA 167.4333 10.180000 76.90000

> aqwm <- dcast(aql,month~variable,fun.aggregate = mean,na.rm=TRUE)
> head(aqwm)
  month    ozone  solar.r      wind     temp
1     5 23.61538 181.2963 11.622581 65.54839
2     6 29.44444 190.1667 10.266667 79.10000
3     7 59.11538 216.4839  8.941935 83.90323
4     8 59.96154 171.8571  8.793548 83.96774
5     9 31.44828 167.4333 10.180000 76.90000
```

##### tidyr

1. `gather`    — 宽数据转为长数据。类似于`reshape2`包中的`melt`函数
2. `spread`    — 长数据转为宽数据。类似于`reshape2`包中的`cast`函数
3. `unit`        — 多列合并为一列
4. `separate ` — 将一列分离为多列

###### **spread**

```R
spread(data, key, value, fill = NA, convert = FALSE, drop = TRUE)
#其中key列就是分类列，value列是该分类列的值，要求key值不重复
```

###### **gather**

```R

```

###### **unit**

```R

```

###### **separate**

```

```
##### dplyr

见工具部分的描述

##### pandas

原始数据

```python
dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
'''
                   A         B         C         D
2013-01-01  0.670013 -0.221569  1.971167 -0.673699
2013-01-02 -0.474492 -1.020013 -0.744874  1.491498
2013-01-03  1.694402 -0.801795  0.743104 -1.831678
2013-01-04 -0.991665 -0.535272  1.038399  0.280514
2013-01-05 -0.455799 -0.558579  1.529402 -0.897370
2013-01-06  1.418096 -1.215279  1.153839 -1.196297
'''
```

宽变长

```python
c=df.stack()
'''
2013-01-01  A    0.670013
            B   -0.221569
            C    1.971167
            D   -0.673699
2013-01-02  A   -0.474492
            B   -1.020013
            C   -0.744874
            D    1.491498
'''

# 如果存在多个索引，则可以使用level number或者name来unstack
```

> 宽变长也可以使用pd.melt()函数来实现
>
> ```python
> pd.melt(df,id_vars=['A'],value_vars=['B','C'])
> '''
>            A variable     value
> 0   0.189141        B -0.580822
> 1  -0.755850        B  1.826144
> 2  -0.535084        B -0.495651
> 3  -0.523995        B -0.712648
> 4  -0.171448        B -1.380292
> 5   0.675715        B -2.038740
> 6   0.189141        C  0.683856
> 7  -0.755850        C -0.435568
> 8  -0.535084        C  0.063186
> 9  -0.523995        C -0.530271
> 10 -0.171448        C  0.730614
> 11  0.675715        C -0.573751
> '''
> ```
>
> 

长变宽

```python
c.unstack()
'''
                   A         B         C         D
2013-01-01  0.670013 -0.221569  1.971167 -0.673699
2013-01-02 -0.474492 -1.020013 -0.744874  1.491498
2013-01-03  1.694402 -0.801795  0.743104 -1.831678
2013-01-04 -0.991665 -0.535272  1.038399  0.280514
2013-01-05 -0.455799 -0.558579  1.529402 -0.897370
2013-01-06  1.418096 -1.215279  1.153839 -1.196297
'''
# 如果存在多个索引，则可以使用level number或者name来unstack
c.unstack(0)
'''
   2013-01-01  2013-01-02  2013-01-03  2013-01-04  2013-01-05  2013-01-06
A    0.670013   -0.474492    1.694402   -0.991665   -0.455799    1.418096
B   -0.221569   -1.020013   -0.801795   -0.535272   -0.558579   -1.215279
C    1.971167   -0.744874    0.743104    1.038399    1.529402    1.153839
D   -0.673699    1.491498   -1.831678    0.280514   -0.897370   -1.196297
'''

c.unstack(1)
'''
                   A         B         C         D
2013-01-01  0.670013 -0.221569  1.971167 -0.673699
2013-01-02 -0.474492 -1.020013 -0.744874  1.491498
2013-01-03  1.694402 -0.801795  0.743104 -1.831678
2013-01-04 -0.991665 -0.535272  1.038399  0.280514
2013-01-05 -0.455799 -0.558579  1.529402 -0.897370
2013-01-06  1.418096 -1.215279  1.153839 -1.196297
'''

```



### 数据分析

#### 回归分析

在作图中使用平滑曲线，使用smooth几何对象完成。

```r
library(ggplot2)
set.seed(1002)
dsmall <- diamonds[sample(nrow(diamonds),100),]
```

> diamomds数据集在ggplot2包中，因此需要先加载

- 局部多项式回归拟合（LOESS）

局部多项式回归拟合是对两维散点图进行平滑的常用方法，它结合了传统线性回归的简洁性和非线性回归的灵活性。当要估计某个响应变量值时，先从其预测变量附近取一个数据子集，然后对该子集进行线性回归或二次回归，回归时采用加权最小二乘法，即越靠近估计点的值其权重越大，最后利用得到的局部回归模型来估计响应变量的值。用这种方法进行逐点运算得到整条拟合曲线。

> 当数据量超过1000时不推荐使用。

```
qplot(carat,price,data=dsmall,geom=c("point","smooth"),span=0.5) # 默认的平滑使用的loess,span参数控制平滑程度
```

例子：

```r
# 平滑
plot(cars,pch=19)
model1=loess(dist~speed,data=cars,span=0.4)
lines(cars$speed,model1$fit,col='red',lty=2,lwd=2)
model2=loess(dist~speed,data=cars,span=0.8)
lines(cars$speed,model2$fit,col='blue',lty=2,lwd=2)

#　预测和残差分析
x=5:25
predict(model2,data.frame(speed=x))
plot(model2$resid~model2$fit)
```

- gam

```r
qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="gam",formula=y~s(x))         # gam
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="gam",formula=y~s(x,bs="cs")) # gam 大数据使用
```

- lm

```r
qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~x)             # lm 线性拟合
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~poly(x,5))     # lm 多项式拟合
  library(splines)
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~ns(x,5))       # lm 多项式样条拟合
```

- rlm

```r
 qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="rlm",formula=y~ns(x,5))       # rlm对噪声不敏感
```

##### 线性回归

//待补充

##### 多元回归

//待补充

##### 逻辑回归

#### 分布分析

##### 正太分布

//待补充

##### 二项分布

//待补充

##### 泊松分布

//待补充

#### 方差分析

//待补充

#### 时间序列

//待补充

### 专题处理

#### 命令行数据处理

安装相关工具箱(除linux本身提供的命令外)

##### 工具准备

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

> 在使用命令的时候提示[warning的解决办法](https://blog.csdn.net/liangzuojiayi/article/details/78213451)：
>
> ```python
> import warnings
> warnings.filterwarnings("ignore")
> ```

###### csvtotable

```shell
pip install csvtotable
```

提供的命令有：

```shell
/usr/bin/csvtotable
```

###### jq

json格式数据处理工具

```shell

```

###### q

类似sql的分割符文本处理

```shell

```

##### 数据处理

###### Obtaining Data

```shell
# 从mysql中导出数据成csv格式
sql2csv --db 'mysql://root:root@localhost/test' --query 'select * from orders'
```

###### Scrubbing Data

```shell

```

###### Exploring Data

```shell

```

###### Modeling Data

```shell

```

###### Interpreting Data

```shell

```

#### 海量数据处理

//这个必须作为一个专题来讲，参考面试之法，编程之道部分

##### 排序

//待补充

##### 查找

1亿条记录数据(有重复)，查找出现最多的10条

 ##参考

- **理论**

  [相关系数](http://m.blog.csdn.net/ciedecem/article/details/39582635)

  [数据科学完整学习路径-Python版（推荐）](https://www.tuicool.com/articles/QBZzquY)

- **工具**

  - Python

    [Pandas操作手册（推荐）](https://www.jianshu.com/p/5142aab20550)

    [十分钟Pandas入门(推荐)](http://pandas.pydata.org/pandas-docs/stable/10min.html)

    [Pandas最神奇的功能](https://mp.weixin.qq.com/s/y6Sy2OV6b-25thHPRC30Tg)

    [Pandas数据规整](https://blog.csdn.net/liujianfei526/article/details/50464614)

    [Numpy入门教程](https://www.jb51.net/article/49397.htm)

  - R

    [R的案列学习（Github）推荐](https://github.com/ljtyduyu/DataWarehouse/tree/master/File)

  - Julia

    [Julia语言初体验](https://mp.weixin.qq.com/s/y_FvuoGLRYNC9B5N0zWEpw)

- **清洗转换**

  - Python

  - R

    [reshape2长宽格式转换](http://www.jianshu.com/p/31d4512ed97f)

    [R语言高效数据清理工具包dplyr](http://www.xueqing.tv/course/31)

    [tidyr包-reshape2包的进化版](http://www.xueqing.tv/cms/article/105)

    [高效数据整理工具包dplyr](https://www.jianshu.com/p/7de1429a2f47)

    [table函数的数据输出转化](https://www.zhihu.com/question/46661384)

- **数据分析**

  - Python

  - R

    [Github的时间序列预测工具prophet](https://github.com/facebook/prophet)

    [在R语言中进行局部多项式回归拟合（LOESS）](http://www.dataguru.cn/article-1525-1.html)

- **专题处理**

  [DataScienceAttheCommandLine](https://github.com/jeroenjanssens/data-science-at-the-command-line)


