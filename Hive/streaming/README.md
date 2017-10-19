##Hive-Streaming
[TOC]

### 基础

#### 原理

mapper和reducer会从标准输入中读取用户数据，一行一行处理后发送给标准输出。Streaming工具会创建MapReduce作业，发送给各个tasktracker，同时监控整个作业的执行过程。

如果一个文件（可执行或者脚本）作为mapper，mapper初始化时，每一个mapper任务会把该文件作为一个单独进程启动，mapper任务运行时，它把输入切分成行并把每一行提供给可执行文件进程的标准输入。 同时，mapper收集可执行文件进程标准输出的内容，并把收到的每一行内容转化成key/value对，作为mapper的输出。 默认情况下，一行中第一个tab之前的部分作为**key**，之后的（不包括tab）作为**value****。**如果没有tab，整行作为key值，value值为null。

对于reducer，类似。

以上是Map/Reduce框架和streaming mapper/reducer之间的基本通信协议。

### 实现

streaming的实现可以用多种语言，此处挑选python,c,shell,perl来实现

#### python实现

调用的python文件需要使用到第三方文件该如何处理

#### shell实现

#### perl实现

#### c/c++实现



 ##参考

[Hadoop Streaming 编程](http://dongxicheng.org/mapreduce/hadoop-streaming-programming/)