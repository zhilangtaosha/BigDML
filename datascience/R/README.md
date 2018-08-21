## R数据统计

[TOC]

R数据分析R包一览：

• ggplot2 - 数据绘图

• dplyr - 数据清洗

• tidyr/reshape2 - 数据转换

• lubridate - 处理日期时间数据

• stringr - 字符串处理

• forcats - 处理类别变量

• readr - 文件读写

### 数据准备

#### 数据接入

//读取各种文件、数据库、网络数据的方式参见r基础部分

#### 数据清理

##### dplyr包

1. 数据筛选-filter函数
2. 子集选取函数-select函数
3. 数据的排序-arrage函数
4. 数据扩展-mutate函数
5. 数据汇总-summarise函数
6. 数据连接-join函数
7. 分类汇总-group by
8. 管道函数
9. 连接MySQL数据库


//详细补充

##### 缺失值处理

缺失的数据量相对数据集的大小来讲比较小，并且为了不偏离分析，忽略少了的样本或许是最后的策略。

在某些情况下，一些快速修复如均值替代或许是不错的办法。对于这种简单的办法，经常会给数据带来偏差。例如，均值代替法对数据的平均值不会产生变化（这是我们所希望的）。但会减小数据的方差，这不是我们所希望的。

而`mice`包通过合理的数据值可以帮我们填充缺失值。这些合理的数据值都是从一个分布中得到的，这个分布是根据缺失数据点的特定情况设计的。

#### 数据转换

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

**spread**

```R
spread(data, key, value, fill = NA, convert = FALSE, drop = TRUE)
#其中key列就是分类列，value列是该分类列的值，要求key值不重复
```

- **gather**

```R

```

- **unit**

```R

```

- **separate**

```

```

### 数理统计

#### 指标

计算均值、方差、中位数、标准差使用函数`mean()`、`var()`、`median()`、`sd`(),这些函数在计算的时候可以根据需要使用`na.rm=TRUE`参数控制是否需要移除空值，`trim`选项用来修剪

```R
# 均值
```

#### 去重

结合使用`duplicated`和`uninque`函数

- vector重复值和非重复值的筛选

```R
x <- round(rnorm(20, 10, 5)) 
#重复值(使用unique的原因是重复值可能出现多次)
unique(x[duplicated(x)]) 
#非重复值
x[!duplicated(x)]
```

- dataframe和matrix重复值和非重复值的筛选

```R
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

#### 排序

- vector排序
- dataframe和matrix按指定的列排序

#### 分组

//待补充

### 回归分析

在作图中使用平滑曲线，使用smooth几何对象完成。

```R
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

```R
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

```R
qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="gam",formula=y~s(x))         # gam
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="gam",formula=y~s(x,bs="cs")) # gam 大数据使用
```

- lm

```R
qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~x)             # lm 线性拟合
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~poly(x,5))     # lm 多项式拟合
  library(splines)
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~ns(x,5))       # lm 多项式样条拟合
```

- rlm

```R
 qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="rlm",formula=y~ns(x,5))       # rlm对噪声不敏感
```

#### 线性回归

//待补充

#### 多元回归

//待补充

#### 逻辑回归

//待补充

### 分布分析

#### 正太分布

//待补充

#### 二项分布

//待补充

#### 泊松分布

//待补充

### 方差分析

//待补充

### 时间序列

//待补充

### 知识积累

#### 函数

##### table函数

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

## 参考

- **数据清洗**

  [reshape2长宽格式转换](http://www.jianshu.com/p/31d4512ed97f)

  [R语言高效数据清理工具包dplyr](http://www.xueqing.tv/course/31)

  [tidyr包-reshape2包的进化版](http://www.xueqing.tv/cms/article/105)

  [table函数的数据输出转化](https://www.zhihu.com/question/46661384)

- **回归分析**

  [在R语言中进行局部多项式回归拟合（LOESS）](http://www.dataguru.cn/article-1525-1.html)

- **知识积累**

  [R的案列学习（Github）推荐](https://github.com/ljtyduyu/DataWarehouse/tree/master/File)

