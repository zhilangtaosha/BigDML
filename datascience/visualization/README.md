##数据可视化
[TOC]

### 基础

#### 问题

##### 是什么？

//待补充

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

###### 例子



##### 柱状图

###### 例子

数据

| 年份   | A    | B    | C    | D    |
| ---- | ---- | ---- | ---- | ---- |
| 2016 | 23   | 232  |      |      |
| 2017 | 1    | 231  | 23   |      |
| 2018 | 232  |      | 232  | 57   |

横柱图

![横柱图](http://tuling56.site/imgbed/2018-03-14_210012.png)

堆叠柱图

![堆叠柱图](http://tuling56.site/imgbed/2018-03-14_210115.png)

##### 线性图

##### 散点图

##### 雷达图

##### 面积图

#### 应用场景

##### 定量分析

1、定量分析(4大类)
​	a、趋势图：时间序列，纵向对比分析
​	b、饼图：成分分析
​	c、条形图：对比分析，纵向对比分析
​	d、散点图：集中度趋势分析、预测分析

##### 定性分析

2、定性分析：[echarts.baidu.com](http://echarts.baidu.com/)
​	a、仪表盘
​	b、雷达图
​	c、漏斗图
​	d、地图
​	e、树状图

#### 绘图流程

![流程](http://tuling56.site/imgbed/2018-03-14_203759.png)

##### 确定主题

##### 确定关系

##### 选择图表

### 实现

#### python-matplotlib

//待补充

#### r-ggplot2

//待补充

#### js-echarts...

//待补充

#### excel-manual、vba

//excel各种类型的图标和所适合的表达关系要逐渐熟悉掌握

 ##参考

- 基础

  [用图表说话-麦肯锡商务沟通.pdf](//带添加)

  [陈为《数据可视化》书评及思维导图](https://www.cnblogs.com/zhangdi/p/3735125.html)

- 进阶

- 实现

  [matplotlib gallary](https://matplotlib.org/gallery.html)

  [ggplot2 gallary](http://www.r-graph-gallery.com/portfolio/ggplot2-package/)

  [echarts gallary](http://echarts.baidu.com/echarts2/doc/example.html)