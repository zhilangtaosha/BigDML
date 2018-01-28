##Hadoop笔记
[TOC]

### 基础

#### 命令积累

文件大小

```shell
hadoop dfs -du -h /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test;
#或者
hdfs  dfs -du -h /user/root/warehouse/xmp_data_mid.db/xmpplaydur_test;

#第一列标示该目录下总文件大小
#第二列标示该目录下所有文件在集群上的总存储大小和你的副本数相关，我的副本数是3 ，所以第二列的是第一列的三倍 （第二列内容=文件大小*副本数）
#第三列标示你查询的目录
```



 ##参考

- 基础

  [hadoop dfs命令大全](http://blog.csdn.net/wuwenxiang91322/article/details/22166423)