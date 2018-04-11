##Map-Reduce
[TOC]

### 基础

​	尽管Hadoop框架是用java写的，但是Hadoop程序不限于java，可以用python、C++、ruby等。本例子中直接用python写一个MapReduce实例，而不是用Jython把python代码转化成jar文件。

​      例子的目的是统计输入文件的单词的词频。

- 输入：文本文件
- 输出：文本（每行包括单词和单词的词频，两者之间用'\t'隔开）

> 其本质是hadoop streaming编程

### 实现

#### python实现





 ##参考

[Python写map-reduce函数](http://www.cnblogs.com/kaituorensheng/p/3826114.html)