##大数据笔记
[TOC]

### 基础

#### 搭建

##### hadoop环境

hadoop=hdfs+mapreduce

##### spark环境

spark=hdfs+spark

spark也是基于hdfs文件系统的，不同的时候spark不使用map-reduce模型

spark是由Berckley的AMPLab实验室使用Scala开发的基于内存的迭代框架。

###### 单机部署

在网址http://spark.apache.org/downloads.html下载预编译的版本，直接解压。然后配置环境变量

```shell
vim ~/.bashrc

export SPARK_HOME=''
export PATH="${SPARK_HOME}/bin:$PATH"

source ~/.bashrc 
```

启动

```shell
pyspark 或者 spark-shell

# 方式1：单机单核
$spark-shell
scala> 1024+3
res1: Int = 1027

$pyspark
>>> 1023+3
1026

# 方式2：单机多核
spark-shell --master local[8]
pyspark --master local[*]
```

> 备注：也可配置ipython支持，参考《全栈数据之门》的0x07

注意启动进入环境之后的提示：

```shell
SparkContext available as sc, HiveContext available as sqlContext.
```

例子：单词计数

```

```

###### 分布式部署

复制单机部署，然后启动的时候以集群的方式

启动

```
spark-shell --master yarn-client
pyspark --master yarn-client
```

提交

```shell

```

#### 生态

生态部分，只是基础的介绍和使用，核心和进阶的操作在进阶部分完成

##### hadoop生态

###### hive

此处要重点关注下hive的原理

###### cassandra

类似于hbase，主要为线上业务服务的

###### hbase

hbase是分布式数据库，是为线上业务服务的，hive是分布式数据仓库，是为了数据分析服务的。

hbase是列数据库，而mysql是行数据库，对于只取某些列数据，在性能上具有明显的优势。

###### Zeppelin

Zeppelin不依赖Hadoop集群环境，可以部署到<u>单独的节点</u>上进行使用。

##### spark生态

不同于传统的map-reduce模型，spark是基于内存迭代的。spark的三个标签：

- 全栈框架
- 分布式
- 内存计算

spark原生提供4种api:scala、java、python、R.

Spark的全栈技术栈

![spark技术栈](http://tuling56.site/imgbed/2018-10-13_145155.png)

###### RDD

两个重要概念，sc=SparkContext和RDD弹性数据集模型

两个基本算子：transform和action

tansform算子

- map():映射，类似于python的map函数
- filter():过滤，类似于python的filter函数
- reduceByKey():按key进行合并
- groupByKey():按key进行聚合

action算子：

- first():返回RDD里面的第一个值
- take(n):从RDD里面取出前n个值
- collect():返回全部的RDD元素
- sum():求和
- count():求个数

###### Spark-SQL

SQL和DataFrame是作为一个整体出现在Spark1.0中的。

**命令行**

SQL的命令行工具为spark-sql.类似于hive的命令行， spark-sql可以读取hive的源数据，因此可以像hive那样对hive表进行操作，并能执行大部分的hive语句 

HIVE交互

```mysql
# 读取hive数据
# 写入数据到Hive
```

MySQL/PostgreSQL

```shell
# 读取mysql数据
# 写数据到mysql
```

其他

```
# 读写json、ORC、Parquet等格式的数据
```

### 进阶

#### hadoop

##### 文件操作

文件信息

```shell
hadoop dfs -du [-s] -h /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test;
#或者
hdfs  dfs -du [-s] -h /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test;

#第一列标示该目录下总文件大小
#第二列标示该目录下所有文件在集群上的总存储大小和你的副本数相关，我的副本数是3 ，所以第二列的是第一列的三倍 （第二列内容=文件大小*副本数）
#第三列标示你查询的目录
 [-s]参数用来求总计的大小，不详细列出子目录的大小
 
# 若不添加协议说明，则默认读取的是hadoop集群上的文件
hadoop fs -ls /user/kankan/yjm/udf
```

> hive执行hdfs命令:
>
> ```shell
> ${HIVE} -e  "dfs -du /x/${checktbl}/ds=${date}"|grep -v items >./temp 2>/dev/null
> ```

文件内容

```shell
#cat
#使用方法：hadoop fs -cat URI [URI …],将路径指定文件的内容输出到stdout
hadoop fs -cat /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test/xxx.gz

#text
#使用方法：hadoop fs -text <src> 
#将源文件输出为文本格式。允许的格式是zip和TextRecordInputStream。
hadoop fs -text /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test/xxx.gz
```

文件操作

```shell
#　文件删除
hadoop fs -rm /home/hadoop/output/lzw
hadoop fs -rmr /home/hadoop/output
hadoop fs -rm  hdfs:///user/kankan/yjm/udf/map.data2

# 文件上传
hadoop fs –put <localsrc> <dst>  # 从本地系统拷贝文件到DFS
```

#### hive

//此部分参考hive手册

#### hbase

hbase是分布式数据库，是为线上业务服务的，不同于hive是数据仓库，是为数据分析服务的。hbase同时也是列式数据库，在集群结构上是主从结构。

##### 基础

###### 运行

```shell
# 进入hbase环境
hbase shell

# 由于hbase没有提供类似hive的-e和-f方式，可使用以下方式变通
echo 'get "gaokao:studete",1111' |hbase shell

# 此外也可以将多个命令写入文件，而文件作为hbase shell的参数来使用
hbase shell xxxx.cmd
```

###### 操作

结构

> hbase也有数据库的概念，是为了逻辑上组合一堆表而用，只不过叫namespace

```mysql
# 查看所有表
list

# 创建数据库
create_namespace 'gaokao'

# 创建表
create 'gaokao:student','info','course','pred'

# 查看表结构
desc 'gaokao:student'

# 增加索引簇(增加addr索引簇，但是VERSIONS的意义不明确)
alter 'gaokao:student',NAME=>'addr',VERSIONS=>3

# 删表(先disable再drop)
disable 'gaokao:student'
drop 'gaokao:student'
```

插入

```shell
# 需要逐列插入，同时插入的时候必须指定行号和索引簇
put 'gaokao:student','1111','info:name','joy'
put 'gaokao:student','1111','info:sex','boy'
```

> 如果插入错误话，没有修改的命令，重新用正确插入覆盖即可

获取

```shell
# 获取的是整行的值，能否获取单列的值？
get 'gaokao:student','11111'
```

删除

```shell
# 单列删除
delete 'gaokao:student','1111','info:sex'

# 整行删除
deleteall 'gaokao:student','1111'
```

##### 数据导入

###### shell

```shell

```

###### hive

```mysql
关联hive表之后，操作hive表就相当于操作hbase，只不过有些细微的不同
```

###### hdfs

```shell
hbase提供的ImportTsv命令
```

###### sqoop

sqoop是连接sql和nosql的桥梁，此处当然可以使用于mysql和hbase场景下

```
从mysql导入到hbase
```

#### spark

##### Spark-SQL

//待补充

#### flume

#### kaflka

 ##参考

- **基础**

  [Zeppelin插件的安装和使用](https://www.cnblogs.com/smartloli/p/5148941.html)

- **进阶**

  - hadoop部分

    [hadoop dfs命令大全](http://blog.csdn.net/wuwenxiang91322/article/details/22166423)

    [hdfs命令大全2](http://www.aboutyun.com/thread-5603-1-1.html)

    [三种恢复 HDFS 上删除文件的方法](https://www.iteblog.com/archives/2321.html)

  - hive部分

    [mapreduce过程详解](http://www.aboutyun.com/thread-7477-1-1.html)

  - hbase部分