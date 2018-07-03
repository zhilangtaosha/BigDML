## R数据可视化

[TOC]

### 图形类型

#### 线性图

![线性图](http://img.phperz.com/data/img/20160102/1451726782_8806.jpg)

#### 饼图

![饼图](http://img.phperz.com/data/img/20160102/1451726792_1808.jpg)

#### 条形图

![条形图](http://img.phperz.com/data/img/20160102/1451726389_7153.png)

#### 柱状图

柱状图代表分时段进入范围的变量值的频率。柱状图类似于条形图表但不同的是它组织中的值为连续范围。在柱状图的每个条代表存在于该范围内的值的数量的高度。

```R
# Create data for the graph.
v <- c(9,13,21,8,36,22,12,41,31,33,19)

# Give the chart file a name.
png(file = "histogram_lim_breaks.png")

# Create the histogram.
hist(v,xlab="Weight",col="green",border="red",xlim = c(0,40), ylim = c(0,5), breaks = 5 )

# Save the file.
dev.off()
```

![柱状图](http://img.phperz.com/data/img/20160102/1451726782_3649.png)

#### 箱线图

箱线图是分布在一个数据集中的数据的量度。它把组分为三个四分位值的数据。此图表示的最小值，最大值，中值，第一个四分位数和第三个四分位数中的数据集。在通过拉伸箱图比较每个跨数据集数据的分布是有用的。

```R
# Give the chart file a name.
png(file = "boxplot_with_notch.png")

# Plot the chart.
boxplot(mpg ~ cyl, data=mtcars,
        xlab="Number of Cylinders",
        ylab="Miles Per Gallon",
        main="Mileage Data",
        notch=TRUE,
        varwidth=TRUE,
        col=c("green","yellow","purple"),
        names=c("High","Medium","Low"))

# Save the file.
dev.off()
```



![箱线图](http://img.phperz.com/data/img/20160102/1451726782_1853.png)

#### 散点图

##### 散点图

![基本散点图](http://img.phperz.com/data/img/20160102/1451726782_9854.png)

##### 散点图矩阵

![散点图矩阵](http://cos.name/wp-content/uploads/2009/03/pairs.png)

```R 
pairs(iris[1:4], main = "Anderson's Iris Data -- 3 species",
      pch = 21,
      bg = c("red", "green3", "blue")[unclass(iris$Species)])
```

[散点图矩阵](http://cos.name/2009/03/scatterplot-matrix-visualization/)的说明：

> 详细的介绍了鸢尾花的花瓣、花萼的长宽和大体的分布，及他们两两之间的关系
>
> 比如第一行第二列的数据：Y轴是Sepal.Length,X轴是Sepal.Width,不同颜色的点代表不同的鸢尾花的不同种类，其它数据类似.

### 函数

#### 高水平

##### plot

plot是一个泛型函数，它产生的图形依赖于第一个参数的类型

##### dotchart

点图

```R
## 基本实现，可用于检测离群点 
dotchart(mtcars$mpg,labels=row.names(mtcars),cex=.7, main="Gas Milage for Car Models",  
   xlab="Miles Per Gallon") 

 

## 按mpg进行排序，按cylinder进行分组并设定不同的颜色，可用于确定聪明变量 
x <- mtcars[order(mtcars$mpg),] # sort by mpg 
x$cyl <- factor(x$cyl) # it must be a factor 
x$color[x$cyl==4] <- "red" 
x$color[x$cyl==6] <- "blue" 
x$color[x$cyl==8] <- "darkgreen"  
dotchart(x$mpg,labels=row.names(x),cex=.7,groups= x$cyl,main="Gas Milage for Car 
Models\ngrouped by cylinder",xlab="Miles Per Gallon", gcolor="black", color=x$color)
```

##### hist

直方图

```R

```

##### density

核密度图

```R

```

##### boxplot

盒图

```R

```

##### barplot

条图

```R

```

##### pie

饼图

```R
 ## 基本实现，绘制饼图并设置标签 
  slices <- c(10, 12,4, 16, 8) 
  lbls <- c("US", "UK", "Australia", "Germany", "France") 
  pie(slices, labels = lbls, main="Pie Chart of Countries") 
  
  
  
  ## 设置百分比标签、颜色 
  slices <- c(10, 12, 4, 16, 8)  
  lbls <- c("US", "UK", "Australia", "Germany", "France") 
  pct <- round(slices/sum(slices)*100) 
  lbls <- paste(paste(lbls, pct) ,"%",sep="") # ad % to labels  
  pie(slices,labels = lbls, col=rainbow(length(lbls)),main="Pie Chart of Countries")  
  
  
  
  ## 3D饼图 
  library(plotrix) 
  slices <- c(10, 12, 4, 16, 8)  
  lbls <- c("US", "UK", "Australia", "Germany", "France") 
  pie3D(slices,labels=lbls,explode=0.1,main="Pie Chart of Countries ") 
```

##### plot/scatterplot/pairs

散点图

```R
## 基本实现-使用plot() 
plot(mtcars$wt, mtcars$mpg, main="Scatterplot Example", xlab="Car Weight ", ylab="Miles 
Per Gallon ", pch=19) 
abline(lm(mtcars$mpg~mtcars$wt), col="red") # 添加回归线 

## 散点图矩阵 
pairs(~mpg+disp+drat+wt,data=mtcars, main="Simple Scatterplot Matrix") 

## 3D散点图 
library(scatterplot3d) 
scatterplot3d(mtcars$wt,mtcars$disp,mtcars$mpg, main="3D Scatterplot") 
```

##### coplot

条件图

paris只能显示双向关系，而coplot函数能够说明三向甚至四向关系，它特别适合观察当给定其它预测变量时，反映变量如何根据一个预测变量变化

```R
## 单个条件变量的条件图 
coplot(mtcars$wt ~ mtcars$mpg | 
as.factor(mtcars$cyl), main="", xlab="", ylab="", 
pch=19) 

 

## 两个条件变量的条件图 
coplot(mtcars$wt ~ mtcars$mpg | 
as.factor(mtcars$cyl) * as.factor(mtcars$vs), 
main="", xlab="", ylab="", pch=19) 
```

##### qqnorm

茎叶图

```R
## 设置绘图参数、准备数据 
par(mfrow = c(1, 2)) 
x = rnorm(100) 

## 绘制Q-Q图 
qqnorm(x, cex = 0.7, asp = 1, main = "", xlim = c(-3,3), ylim=c(-3,3)) 
abline(0, 1,col='red') 

## 绘制数据密度曲线 
plot(density(x), main = "", xlim = c(-3,3), ylim=c(0,0.4)) 

## 绘制实际正态分布密度曲线 
curve(dnorm, from = -3, to = 3, lty = 2, add = TRUE, col='red') 
```

##### map

```R
## 地图绘制相关包 
library(maps) 
library(mapdata) 
library(maptools) 

## 读取地图数据 
x <- readShapeSpatial('E:\\map\\bou2_4m\\bou2_4p') 

## 用不同的颜色绘制地图 
par(mar=c(0,0,0,0)) 
plot(x,col=rainbow(n=33)); 
```

##### ** 绘图参数设置**

指定方式

```
方式一：在高级绘图函数中直接指定 
hist(mtcars$mpg, col.lab="red") 
更多高水平绘图函数的参数参加具体的函数（如hist/boxplot/plot等等） 

方式二：通过par()函数 
par()                     	# 查看当前绘图参数设置 
opar <- par()        		# 保存当前设置 
par(col.lab="red") 			# 设置坐标轴标签为红色  
hist(mtcars$mpg) 			# 利用新的参数绘图 
par(opar)              		# 恢复绘图参数的原始设置 
```

设置文本和符号的大小

```

```

设置点的类型

```

```

设置线性的类型

```

```

设置颜色

```

```

设置字体

```

```

设置图形边缘大小

```

```

#### 低水平

低水平绘图函数:点、直线、线段、箭头、网格线

| 函数名称           | 描述                                       |
| -------------- | ---------------------------------------- |
| points         | 增加点                                      |
| lines          | 增加连接线                                    |
| abline(a,b)    | 增加一个斜率为b,截距为a的直线                         |
| abline(h=y)    | h=y可用于指定贯穿整个图的水平线高度的y-坐标                 |
| abline(v=x)    | v=x类似地用于指定垂直线的x-坐标                       |
| abline(lm:obj) | lm:obj 可能是一个有长度为2的coefficients 分量(如模型拟合的结果)的 |
| segments       | 绘制点对之间的线段                                |
| arrows         | 绘制点对之间的箭头                                |
| grid           | 在当前绘图区增加网格线                              |

##### 基本图形

```R
## 基本实现 
plot(-4:4, -4:4, type = "p", col="blue") 

## 绘制点、连接点 
points(x=c(3,-2,-1,3,2), y=c(1,2,-2,2,3), col = "red") 
lines(x=c(3,-2,-1,3,2), y=c(1,2,-2,2,3),col="black") 

## 绘制直线 
abline(h=0) 
abline(v=0) 
abline(a=1,b=1) 
abline(lm(mtcars$mpg ~ mtcars$qsec),col="red") 

## 绘制线段 
segments(x0=2, y0=-4.5, x1=4, y1=-2, col="red", lty="dotted") 

## 绘制箭头,并设置箭头的长度、角度、样式 
arrows(x0=-4, y0=4, x1=-2, y1=0, length=0.15, angle=30, code=3) 

##绘制网格线 
grid(nx=3, ny=5, col = "lightgray", lty = "dotted") 
```

多边形和矩形

```R
#绘制由(x,y)作为顶点的多边形的低水平函数如下： 
polygon(x, y = NULL, density = NULL, angle = 45, border = NULL, col = NA, lty = par("lty"), fillOddEven = FALSE)  

#对于多边形的特例矩形，R还提供了专门的函数rect()来绘制： 
rect(xleft, ybottom, xright, ytop, density = NULL, angle = 45, 
     col = NA, border = NULL, lty = par("lty"), lwd = par("lwd"),...) 

## 基本实现 
plot(-4:4, -4:4, type = "p", col="blue") 
polygon(x=c(3,-2,-1,3,2), y=c(1,2,-2,2,3), col = "red") # 绘制多边形 
rect(xleft=c(-4,0), ybottom=c(2,-4), xright=c(-2,2), ytop=c(4,-2), col = c("blue", "yellow")) # 绘制两个矩形，并填充颜色 
```

##### 标题和文本

```R
## 使用title()函数添加红色标题和蓝色子标题，设置坐标轴标签为绿色，字体相对大小为0.75 
plot(mtcars$wt,  mtcars$mpg, main='',sub='',xlab='',ylab='') 
title(main="My Title", col.main="red", sub="My Sub-title", col.sub="blue", xlab="My X label", 
ylab="My Y label", col.lab="green", cex.lab=0.75) 

 

## 使用text()/mtext()函数为绘图区域/边缘区域添加文本注释 
plot(x=mtcars$wt, y=mtcars$mpg, main="Milage vs. Car Weight", xlab="Weight", 
ylab="Mileage", pch=18, col="blue") 
text(x=mtcars$wt, y=mtcars$mpg, labels=row.names(mtcars), cex=0.6, pos=4, col="red") 
mtext("Added by mtext()", side=2, line=2,col='blue') 
```

##### 坐标轴和图例

```R
##添加坐标轴 
x <- c(1:10); y <- x; z <- 10/x 
par(mar=c(5, 4, 4, 8) + 0.1) 
plot(x, y,type="b", pch=21, col="red", yaxt="n", lty=3, xlab="", ylab="") 
lines(x, z, type="b", pch=22, col="blue", lty=2) 
axis(side=2, at=x,labels=x, col.axis=“red”, las=2) # 左侧添加坐标轴，设置坐标轴刻度标签样
式 
axis(side=4, at=z,labels=round(z,digits=2), col.axis="blue", las=2, cex.axis=0.7, tck=-.01) # 
右侧添加坐标轴，设置坐标轴标签及刻度线的长度 
mtext("y=1/x", side=4, line=3, cex.lab=1,las=2, col="blue") 
title("An Example of Creative Axes", xlab="X values", ylab="Y=X") 

 
## 添加图例，并设置格式 
counts <- table(mtcars$vs, mtcars$gear) 
barplot(counts, main="Car Distribution by Gears and VS",xlab="Number of Gears", 
col=c("darkblue","red"), beside=TRUE) 
legend(x=7.5, y=12, legend=c("L-A","L-B"), pch=15, col=c("blue","red"), cex=0.8, pt.cex=1, 
box.lty="dashed") 

```

#### 交互式

#### 组合图形

##### par

###### mfrow和mflcol参数

```R
## 使用frow/fcol 
mypar <- par(mfrow=c(2,2)) 
plot(mtcars$wt,mtcars$mpg, main="Scatterplot of wt 
vs. mpg") 
plot(mtcars$wt,mtcars$disp, main="Scatterplot of wt 
vs disp") 
hist(mtcars$wt, main="Histogram of wt") 
boxplot(mtcars$wt, main="Boxplot of wt") 
par(mypar) 
```

###### fig参数

使用par()函数的fig参数 

-  fig参数的值是一个形如c(x1,x2,y1,y2)的数值型向量，指定各个图形的绘制位置 
-  new参数是一个逻辑指，指定是否将图形绘制到已有图形

```R
## 在散点图上添加盒图 
par(fig=c(0,0.8,0,0.8), new=FALSE) 
plot(mtcars$wt, mtcars$mpg, xlab="Miles Per Gallon", ylab="Car Weight") 
par(fig=c(0,0.8,0.55,1), new=TRUE) 
boxplot(mtcars$wt, horizontal=TRUE, axes=FALSE) 
par(fig=c(0.65,1,0,0.8),new=TRUE) 
boxplot(mtcars$mpg, axes=FALSE) 
mtext("Enhanced Scatterplot", side=3, outer=TRUE, line=-3)  
```

##### layout

使用layout(mat, widths = rep(1, ncol(mat)),heights = rep(1, nrow(mat)), respect = FALSE)函数 

```R
## 基本实现 
attach(mtcars) 
layout(mat=matrix(c(1,1,2,3), 2, 2, byrow = TRUE), widths=c(3,1), heights=c(1,2)) 
layout.show(3) 
hist(wt) 
hist(mpg) 
hist(disp) 
```

#### 高级格函数（Lattice）

Lattice是自带的绘图函数库,该库带的高级函数一览:

| 函数          | 描述      | 备注   |
| ----------- | ------- | ---- |
| histogram   | 直方图     |      |
| densityplot | 核密度图    |      |
| qqmath      | 理论分位数图  |      |
| qq          | 双样本分位数图 |      |
| stripplot   | 带形图     |      |
| bwplot      | 盒图      |      |
| dotplot     | 克里夫兰点图  |      |
| barchart    | 条形图     |      |
| xyplot      | 散点图     |      |
| splom       | 散点图阵列   |      |
| contourplot | 表面等高线图  |      |
| levelplot   | 表面伪色彩图  |      |
| wireframe   | 三维表面透视图 |      |
| cloud       | 三维散点图   |      |
| parallel    | 平行坐标图   |      |

例子：

```R
## 加载包 
library(lattice)  


## 创建gear对应的因子类型变量 
attach(mtcars) 
gear.f <- factor(gear,levels=c(3,4,5), 
labels=c("3gears","4gears","5gears"))  


## 按gear.f绘制mpg的多面板盒图 
bwplot(x=~ mpg|gear.f, main="Boxplot by Gears", xlab="Miles per Gallon", layout=c(3,1)) 


## 按gear.f绘制mpg~wt的多面板散点图 
xyplot(x=mpg~wt|gear.f, main= "Scatterplots by Gears", xlab="Miles per Gallon", layout=c(3,1)) 
```

### 绘图库

#### qplot

#### ggplot2

#### plotly

//交互式强

##  参考

- 基础
- 函数
- 绘图库