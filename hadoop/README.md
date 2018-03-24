##Hadoop笔记
[TOC]

### 基础

#### 命令

文件大小

```shell
hadoop dfs -du [-s] -h /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test;
#或者
hdfs  dfs -du [-s] -h /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test;

#第一列标示该目录下总文件大小
#第二列标示该目录下所有文件在集群上的总存储大小和你的副本数相关，我的副本数是3 ，所以第二列的是第一列的三倍 （第二列内容=文件大小*副本数）
#第三列标示你查询的目录
 [-s]参数用来求总计的大小，不详细列出子目录的大小
```

删除

```
hadoop fs -rm /home/hadoop/output/lzw
hadoop fs -rmr /home/hadoop/output
```

HIVE执行hdfs命令

```shell
${HIVE} -e  "dfs -du /user/kankan/warehouse/xmp_odl.db/${checktbl}/ds=${date}/hour=${checkhour}/"|grep -v items >./temp 2>/dev/null
```

上传

```shell
hadoop fs –put <localsrc> <dst>  # 从本地系统拷贝文件到DFS
```



 ##参考

- 基础

  [hadoop dfs命令大全](http://blog.csdn.net/wuwenxiang91322/article/details/22166423)

  [hdfs命令大全2](http://www.aboutyun.com/thread-5603-1-1.html)

  [三种恢复 HDFS 上删除文件的方法](https://www.iteblog.com/archives/2321.html)