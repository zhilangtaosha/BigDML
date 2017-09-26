##PySpark
[TOC]

### 基础

#### 安装

```shell
pip install --index http://pypi.douban.com/simple/  --trusted-host pypi.douban.com  pyspark
#pyspark依赖py4j，在安装的时候会自动安装py4i库
#Successfully installed py4j-0.10.4 pyspark-2.2.0
```

#### 结构介绍

子包介绍

- [pyspark.sql module](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html)
- [pyspark.streaming module](http://spark.apache.org/docs/latest/api/python/pyspark.streaming.html)
- [pyspark.ml package](http://spark.apache.org/docs/latest/api/python/pyspark.ml.html)
- [pyspark.mllib package](http://spark.apache.org/docs/latest/api/python/pyspark.mllib.html)

公共类介绍

- - [`SparkContext`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.SparkContext):

    Main entry point for Spark functionality.

- - [`RDD`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.RDD):

    A Resilient Distributed Dataset (RDD), the basic abstraction in Spark.

- - [`Broadcast`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.Broadcast):

    A broadcast variable that gets reused across tasks.

- - [`Accumulator`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.Accumulator):

    An “add-only” shared variable that tasks can only add values to.

- - [`SparkConf`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.SparkConf):

    For configuring Spark.

- - [`SparkFiles`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.SparkFiles):

    Access files shipped with jobs.

- - [`StorageLevel`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.StorageLevel):

    Finer-grained cache persistence levels.

- - [`TaskContext`](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.TaskContext):

    Information about the current running task, avaialble on the workers and experimental.

入门示例



 ##参考

[PySpark内容介绍](http://www.cnblogs.com/wenBlog/p/6323678.html)

[pyspark官方文档](http://spark.apache.org/docs/latest/api/python/pyspark.html#module-pyspark)

[pyspark经典入门教程系列](http://www.mccarroll.net/blog/pyspark2/)