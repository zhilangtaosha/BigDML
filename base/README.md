##大数据笔记
[TOC]

### 基础

#### 基础环境

##### hadoop环境

##### spark环境

#### 生态环境

##### hadoop生态

###### hive

###### cassandra

###### hbase

hbase是分布式数据库，是为线上业务服务的，hive是分布式数据仓库，是为了数据分析服务的。

hbase是列数据库，而mysql是行数据库，对于只取某些列数据，在性能上具有明显的优势。

##### Zeppelin

Zeppelin不依赖Hadoop集群环境，可以部署到<u>单独的节点</u>上进行使用。

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
```

> hive执行hdfs命令:
>
> ```shell
> ${HIVE} -e  "dfs -du /x/${checktbl}/ds=${date}"|grep -v items >./temp 2>/dev/null
> ```

文件内容

```shell
hadoop fs -cat /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test/xxx.gz
```

文件操作

```shell
#　文件删除
hadoop fs -rm /home/hadoop/output/lzw
hadoop fs -rmr /home/hadoop/output

# 文件上传
hadoop fs –put <localsrc> <dst>  # 从本地系统拷贝文件到DFS
```

#### hive

//此部分参考hive手册

#### hbase

##### 基础

```shell
hbase shell
```

#### spark

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