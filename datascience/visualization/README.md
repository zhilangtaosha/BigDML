##数据可视化
[TOC]

### 基础

#### 问题

##### 是什么？

数据可视化的意义是什么？？

##### 怎么学?

《数据之美》、《可视化数据》、 《数据可视化之美》、《鲜活的数据》、《[数据可视化实战:使用D3设计交互式图表](http://www.amazon.cn/%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96%E5%AE%9E%E6%88%98-%E4%BD%BF%E7%94%A8D3%E8%AE%BE%E8%AE%A1%E4%BA%A4%E4%BA%92%E5%BC%8F%E5%9B%BE%E8%A1%A8-%E8%8E%AB%E7%91%9E/dp/B00DMS9FA8/ref=pd_sim_b_4?ie=UTF8&refRID=0S7CBJDS5Z8B5CGV0H5Q)》以及一系列数据挖掘相关的案例及算法书。但最给我有开阔视野、醍醐灌顶之功效的书，还是这本浙大陈为教授等人编著的[大数据丛书:数据可视化](http://www.amazon.cn/%E5%A4%A7%E6%95%B0%E6%8D%AE%E4%B8%9B%E4%B9%A6-%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96-%E9%99%88%E4%B8%BA/dp/B00GDI2SGC/ref=pd_sim_b_2?ie=UTF8&refRID=0ATX0V1SR7K0FKD83X0D)

#### 规范

1、横坐标
​	a. 日期格式 MM/DD（日期数据可以折叠，例如2017/6/12折叠成17/6/12,或者用每月的第一天作为横）
​	b. 日期间隔，时间跨度-看长期趋势
2、纵坐标
​	a. 纵坐标要够高，才能看到波动趋势
​	b. 纵坐标刻度密度
​	c. 纵坐标可读性，大数据建议以万(千)为单位
3、标题
​	a. 图序号
​	b. 图标题是概括性总结
​	c. 单位（应该写在纵轴上）
4、数据
​	a. 数据标签的使用：记录波动原因（待）
​	b. 趋势线使用带标记点的线，不要使用平滑过的（为什么不用平滑的？）
​	c. 颜色配色：多个指标时候，要易于区分
​	d. 不在一个数量级的数据，双坐标的使用
5、收入类数据，年度累计+目标的展现方式。

### 进阶

#### 图表样式

![图表样式](http://tuling56.site/imgbed/2018-03-14_204808.png)

此外参考面积图和雷达图

##### 饼图

###### 饼图成分对比

![饼图成分对比](http://tuling56.site/imgbed/2018-03-14_205232.png)

##### 条形图

![条形图分类](http://tuling56.site/imgbed/2018-03-14_205401.png)



##### 柱状图

数据

| 年份   | A    | B    | C    | D    |
| ---- | ---- | ---- | ---- | ---- |
| 2016 | 23   | 232  |      |      |
| 2017 | 1    | 231  | 23   |      |
| 2018 | 232  |      | 232  | 57   |

###### 横柱图

![横柱图](http://tuling56.site/imgbed/2018-03-14_210012.png)

###### 堆叠柱图

![堆叠柱图](http://tuling56.site/imgbed/2018-03-14_210115.png)

堆积柱图若考虑整体的成分构成，而不是随着年份变话的话，可以考虑使用南丁格尔玫瑰图

![南丁格尔玫瑰图](http://tuling56.site/imgbed/2018-06-20_161044.png)

##### 线性图

时间序列分析、相关分析

##### 散点图

相关分析、分布分析

##### 雷达图

静态多维对比

##### 面积图

数据组成的变化趋势

###### 堆积面积图

队列分析

#### 图表选择

根据是进行定量分析还是定性分析的，初步选择依据如下：

1、定量分析(4大类)
	a、趋势图：时间序列，纵向对比分析
	b、饼图：成分分析
	c、条形图：对比分析，纵向对比分析
	d、散点图：集中度趋势分析、预测分析

2、定性分析：[echarts.baidu.com](http://echarts.baidu.com/)
	a、仪表盘
	b、雷达图
	c、漏斗图
	d、地图
	e、树状图

详细的图表选择依据：

![图表选择依据-方方格子-Excel图表之道](http://tuling56.site/imgbed/2018-08-16_204436.png)



#### 图表细节

##### 细节

###### 背景

###### 坐标轴

###### 辅助线

###### 趋势线

###### 标注线

##### 技巧

###### 组合图表

###### 子母图

###### 迷你图

#### 绘图流程

![流程](http://tuling56.site/imgbed/2018-03-14_203759.png)

##### 确定主题

研究什么

##### 确定关系

确定是什么关系

##### 选择图表

用什么样图表表达这种关系

![反映关系的图标类型](http://tuling56.site/imgbed/2018-06-20_142050.png)

### 实现

#### 编程实现

##### python

主要包含：matplotlib、seaborn、plotly、bokeh

![python数据可视化图](http://tuling56.site/imgbed/2018-06-20_141901.png)

###### matplotlib

```python

```

###### pyecharts

```python

```

###### seaborn

###### plotly

###### bokeh

##### r

主要包含：ggplot2、Lattice

###### ggplot2

```R

```

##### js

主要包含:echarts、plotly、d3.js

###### echarts

###### plotly

###### d3.js

#### 无需编程

##### excel

主要包含：manual、vba

//excel各种类型的图标和所适合的表达关系要逐渐熟悉掌握，看Excel图表之道

##### PowerBI

商业智能:微软出品，包含全套的组件

##### FineBI

商业智能:打开客户端后通过web页面访问

##### Tableau

商业智能:客户端软件实体展现，感觉用着比FineBI好用

### 实战

#### 特殊绘图

##### 四维绘图

![思维绘图study.2d_2i_down](http://tuling56.site/imgbed/2018-06-26_110254.png)

期望输出的绘图

![期望绘图](http://tuling56.site/imgbed/2018-06-26_110907.png)

绘图说明：

> 1. 横坐标时间维不变
> 2. 纵坐标指标维可自由调整

也可以单独绘图，最后对绘图的结果进行拼接，而不一次性的给出绘图结果

 ##参考

- **基础**

  [用图表说话-麦肯锡商务沟通.pdf](//带添加)

  [Excel图表之道-如何制作专业有效的商务图表](//)

  [陈为《数据可视化》书评及思维导图](https://www.cnblogs.com/zhangdi/p/3735125.html)

  [talkingdata移动互联网大数据平台](https://www.talkingdata.com/)

  [Python数据可视化编程实战（书籍）](http://item.jd.com/11676691.html)

- **进阶**

  //补充绘制图表的基本原理

  [数据可视化的十大误区(推荐)](https://www.toutiao.com/a6606090350673003021/?iid=6606090350673003021)

- **演示**

  [matplotlib gallary](https://matplotlib.org/gallery.html)

  [ggplot2 gallary](http://www.r-graph-gallery.com/portfolio/ggplot2-package/)

  [echarts gallary](http://echarts.baidu.com/echarts2/doc/example.html)

  [matplotlib_tutorial](https://github.com/rougier/matplotlib-tutorial)(git仓库)

  [highcharts demo](https://www.highcharts.com/demo)

  [amcharts demo](https://www.amcharts.com/demos/)

  [echarts demo](http://echarts.baidu.com/examples/)