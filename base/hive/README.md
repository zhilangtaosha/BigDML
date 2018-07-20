## HIVE笔记

[TOC]

### 基础

#### 数据类型

基本数据类型：tinyint, smallint, int,bigint, boolean, float, double, string

复杂数据类型：struct，map，array

##### 基本数据类型

| 数据类型      | 所占字节                                     | 开始支持版本          |
| --------- | ---------------------------------------- | --------------- |
| TINYINT   | 1byte，-128 ~ 127                         |                 |
| SMALLINT  | 2byte，-32,768 ~ 32,767                   |                 |
| INT       | 4byte,-2,147,483,648 ~ 2,147,483,647     |                 |
| BIGINT    | 8byte,-9,223,372,036,854,775,808 ~ 9,223,372,036,854,775,807 |                 |
| BOOLEAN   |                                          |                 |
| FLOAT     | 4byte单精度                                 |                 |
| DOUBLE    | 8byte双精度                                 |                 |
| STRING    | 字符串                                      |                 |
| BINARY    |                                          | 从Hive0.8.0开始支持  |
| TIMESTAMP |                                          | 从Hive0.8.0开始支持  |
| DECIMAL   |                                          | 从Hive0.11.0开始支持 |
| CHAR      |                                          | 从Hive0.13.0开始支持 |
| VARCHAR   |                                          | 从Hive0.12.0开始支持 |
| DATE      |                                          | 从Hive0.12.0开始支持 |

**string**

```mysql
# 字符串分割(返回数组)
split('xxx_we2_23','_');  
```

**num**

```mysql
create table if not exists basic_test(
	ia_tiny tinyint unsigned,
    ib_small smallint unsigned,
    ib1_small smallint,
    ic_float float,
    id_double double,
    ie_boolen boolean
);
```

##### 复杂数据类型

###### **array**

```mysql
CREATE TABLE `array_test`(
  `a` array<int>, 
  `b` array<string>)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'colelction.delim'=',', 
  'field.delim'='\t', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  'hdfs://wh-ns/user/root/warehouse/xmp_data_mid.db/array_test';
```

数组索引

```mysql
# 求array的长度
size(array)

# 注意数组的索引下标是从0开始的
 select array('1','2')[0]; # 结果1

# # 如何将计算的数据直接在本行内使用呢(使用子查询的方式达到了结果)
select split("wew_w23_ew0","_")[a.cnt-1] from (select size(split("wew_w23_ew0",'_')) as cnt)a;
```

> 问题是无法对数据采用-1，-2这样的倒序查(已解决)，例子：
>
> ```mysql
> select a.sstr,split(a.sstr,"_")[a.cnt-1] from (select sstr,size(split(sstr,'_')) as cnt from xmp_data_mid.streaming_test limit 10)a;
>
> select a.gcid,split(a.filename,'\\\\')[a.cnt-1] from (select gcid,filename,size(split(filename,'\\\\')) as cnt from xmp_mid.gcid_filename_filter where gcid!='' limit 100)a;
>
> # 两次反转(分割得到的数组取最后一个）
> select reverse(split(reverse('a1,b1,c1,d2'),',')[0]);
> ```
>
> 注意在shell中要换成8个（在hql脚本中和在hive的命令行中保持一样，都是4个），如下：

> ```shell
> hql="select a.gcid,split(a.filename,'\\\\\\\')[a.cnt-1] from (select gcid,filename,size(split(filename,'\\\\\\\')) as cnt from xmp_mid.gcid_filename_filter where gcid!='' limit 100)a;"
> echo "$hql"
> ${HIVE} -e "$hql"
> ```

例子：

```mysql
create table array_test(a array<int>, b array<string>) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' COLLECTION ITEMS TERMINATED BY ',' STORED AS TEXTFILE;

load data local inpath "array.txt"  overwrite into table array_test partition(ds=20180114);
```

数组统计

```shell
# 统计数组中每个元素和其个数
# 求数组中所有元素的和
# 求数组中最大的元素
# 判断一个数是否在数组中
```

###### **map**

```mysql
CREATE TABLE `map_test`(
  `a` string, 
  `b` map<string,string>, 
  `c` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'colelction.delim'=',', 
  'field.delim'='\t', 
  'mapkey.delim'=':', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  'hdfs://wh-ns/user/root/warehouse/xmp_data_mid.db/map_test';
```

map数据的插入

```mysql
select map("key1","val1") from test.dual; 

# 测试1：
insert into table xmp_data_mid.map_test values('hahh',map("key1","val1"),'vvv');
# 则会报错：Unable to create temp file for insert values Expression of type TOK_FUNCTION not supported in insert/values,也即不支持插入原生类型
# 更改成：
insert into table xmp_data_mid.map_test select 'hh',map("key1","val1"),'v' # from test.dual;


# 测试2：
insert into table xmp_data_mid.map_test select 'hahh','{"key2":"val2"}';
# 则会报错：
# FAILED: SemanticException [Error 10044]: Line 1:18 Cannot insert into target table because column number/types are different 'map_test': Cannot convert column 1 from string to map<string,string>.
# 更改成：
insert into table xmp_data_mid.map_test select 'hahh',str_to_map('{"key2":"val2"}'),'v';
hahh    {"{\"key2\"":"\"val2\"}"}  # 插入结果(str_to_map转换的时候注意中括号等要去除)
# 进一步修正： 
insert into table xmp_data_mid.map_test 
select '{"k2":"v2"}',str_to_map(regexp_replace('{"k2":"v2"}','"|\\}|\\{','')),'{k2:v2}';
@@ 查询验证：
select get_json_object(a,'$.k2'),b['k2'],get_json_object(c,'$.k2') from xmp_data_mid.map_test where c='{k2:v2}';  # 结果:v2      v2      NULL,也就是说在插入的是json的key和v一定要带字符串


# 测试3：
insert into xmp_data_mid.map_test select b,b,b from xmp_data_mid.map_test where c='{k2:v2}';
# map的导出形式插入到string时，map会进退化成：k2:v2   {"k2":"v2"}     k2:v2


# 测试4：
insert into table xmp_data_mid.map_test select 'hahh',str_to_map('k6:v6,k8:v8'),'v8';
insert into table xmp_data_mid.map_test
select
    'a'
    ,str_to_map(concat_ws(',',concat('id:',channel_id),concat('code:',channel_code)))
    ,'ccc'
from 
    sl_channel_id_type
limit 10;

```

> map字段插入空:
>
> ```mysql
> insert into xxxx partition(ds = 'xxxxxx')
> select xxx as c1,map(NULL, NULL) as c2 from xxx;
> #select查询时，显示此字段为{}。
> ```

例子：

```mysql
# 建表
create table map_test(a string , b map<string, string>)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE;

#加载
load data local inpath "map.txt"  overwrite into table map_test;
```

> 注意:
>
> map的字典不能直接在order by中使用，需要使用别名
>
> ```mysql
> select mdict['xxx'] as mdx,mdict['vvv'] from db1.table1 order by  mdx;
> ```

map操作

```shell
# map构建
两个等长数组构建map

# map的keys中是否含有某key

# map的values中是否含有某value
```

###### **struct**

```mysql
# 建表
create table struct_test(id INT, info struct<name:STRING, age:INT>)  
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','                         
COLLECTION ITEMS TERMINATED BY ':'
STORED AS TEXTFILE;

# 加载
load data local inpath "struct.txt"  overwrite into table struct_test;
```

例子：

```mysql
select info.age from struct_test;
```

**综合例子：**

```mysql
# 建表
create table group_test(ds string,srctbl string,srcdb string, hour string,datasize int)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE;

# 加载
load data local inpath "group.txt"  overwrite into table group_test;
```

##### 数据类型转换

![隐式数据类型转换](http://tuling56.site/imgbed/2018-03-27_112329.png)

###### 字符串类型

字符串转整型

```
cast(string as int)
```

###### 日期类型 

时间戳转时间戳字符串

```
cast(ts as string)
```

时间戳转日期字符串

```
from_unixtime(ts,''yyyyMMdd HH:mm:ss')
```

###### 整型

整型转字符串

```mysql
cast(xxint as string);
```

进制转换

```mysql

```

#### 属性设置

命令行

```shell
# 静音模式
$HIVE_HOME/bin/hive -S -e 'select a.col from tab1 a'
# #加入-S，终端上的输出不会有mapreduce的进度，执行完毕，只会把查询结果输出到终端上。这个静音模式很实用，,通过第三方程序调用，第三方程序通过hive的标准输出获取结果集。

# 设置
set <key>=<value>	修改特定变量的值
注意: 如果变量名拼写错误，不会报错
set	输出用户覆盖的hive配置变量
set -v	输出所有Hadoop和Hive的配置变量

# 资源和分布式缓存
add FILE[S] <filepath> <filepath>* 
add JAR[S] <filepath> <filepath>* 
add ARCHIVE[S] <filepath> <filepath>*	添加 一个或多个 file, jar,  archives到分布式缓存
list FILE[S] 
list JAR[S] 
list ARCHIVE[S]	输出已经添加到分布式缓存的资源。
list FILE[S] <filepath>* 
list JAR[S] <filepath>* 
list ARCHIVE[S] <filepath>*	检查给定的资源是否添加到分布式缓存
delete FILE[S] <filepath>* 
delete JAR[S] <filepath>* 
delete ARCHIVE[S] <filepath>*

# 执行
! <command>	从Hive shell执行一个shell命令
source FILE <filepath>	在CLI里执行一个hive脚本文件
```

hiveconf参数设置

```shell
HIVE_2="/usr/local/complat/complat_clients/cli_bin/hive  
-hiveconf mapred.job.name=kkstat_hive 
-hiveconf hive.exec.compress.output=true 
-hiveconf hive.groupby.skewindata=false 
-hiveconf hive.exec.compress.intermediate=true 
-hiveconf io.seqfile.compression.type=BLOCK 
-hiveconf mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec 
-hiveconf hive.map.aggr=true 
-hiveconf hive.stats.autogather=false 
-hiveconf hive.exec.scratchdir=/user/kankan/tmp  
-hiveconf mapred.job.queue.name=kankan -S "
```

| 功能                                      | 语法                                       |
| --------------------------------------- | ---------------------------------------- |
| 设置job名称                                 | mapred.job.name=complatstat_hive         |
| 数据压缩是否开启                                | hive.exec.compress.output=true           |
| 中间结果是否压缩                                | hive.exec.compress.intermediate=true     |
| Sequencefile压缩级别                        | io.seqfile.compression.type=BLOCK        |
| 输出压缩方式                                  | mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec |
| 在map端做部分聚集                              | hive.map.aggr=true                       |
| HDFS路径,  存储不同 map/reduce  阶段执行计划和中间输出结果 | hive.exec.scratchdir=/user/complat/tmp   |
| 队列名                                     | mapred.job.queue.name=complat            |
| 支持动态分区                                  | hive.exec.dynamic.partition=true         |
| 允许所有的分区列都是动态分区列                         | hive.exec.dynamic.partition.mode=nonstrict |
| 执行map前开启小文件合并                           | hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat |
| 是否根据输入表的大小自动转成map  join                 | hive.auto.convert.join=false             |
| hive.groupby.skewindata                 | 当数据出现倾斜时，如果该变量设置为true，那么Hive会自动进行负载均衡。   |

#### 表和视图

##### 创建表

```mysql
CREATE [EXTERNAL] TABLE [IF NOT EXISTS] table_name 
  [(col_name data_type [COMMENT col_comment], ...)] 
  [COMMENT table_comment] 
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)] 
  [CLUSTERED BY (col_name, col_name, ...) 
  [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS] 
  [ROW FORMAT row_format] 
  [STORED AS file_format] 
  [LOCATION hdfs_path]
```

> •CREATE TABLE 创建一个指定名字的表。如果相同名字的表已经存在，则抛出异常；用户可以用 IF NOT EXIST 选项来忽略这个异常
> •EXTERNAL 关键字可以让用户创建一个外部表，在建表的同时指定一个指向实际数据的路径（LOCATION）
> •LIKE 允许用户复制现有的表结构，但是不复制数据
> •COMMENT可以为表与字段增加描述
>
> •ROW FORMAT
>     DELIMITED [FIELDS TERMINATED BY char] [COLLECTION ITEMS TERMINATED BY char]
>         [MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char]
>    | SERDE serde_name [WITH SERDEPROPERTIES (property_name=property_value, property_name=property_value, ...)]
>          用户在建表的时候可以自定义 SerDe 或者使用自带的 SerDe。如果没有指定 ROW FORMAT 或者 ROW FORMAT DELIMITED，将会使用自带的 SerDe。在建表的时候，用户还需要为表指定列，用户在指定表的列的同时也会指定自定义的 SerDe，Hive 通过 SerDe 确定表的具体的列的数据。
> •STORED AS
>             SEQUENCEFILE
>             | TEXTFILE
>             | RCFILE    
>             | INPUTFORMAT input_format_classname OUTPUTFORMAT             output_format_classname
>        如果文件数据是纯文本，可以使用 STORED AS TEXTFILE。如果数据需要压缩，使用 STORED AS SEQUENCE 。

创建库的时候最好指定下库的路径，建立内部表的时候不建议指定表的location的位置，如下格式：

```mysql
create database if not exists apple1_bdl comment 'apple1 without xiaomi bdl data'
location '/user/complat/warehouse/apple1_bdl.db/';
```

> 这是创建库而不指定库的路径的时候库的目录是/user/xxx/warehouse/,此处删除库的时候会直接将整个目录删除。

分割符

```mysql
CREATE TABLE ...
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
COLLECTION ITEMS TERMINATED BY '\002'
MAP KEYS TERMINATED BY '\003'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;
```

###### 文本格式

外部表

```sql
use kankan_odl;drop table if exists hive_table_templete;
create external table if not exists hive_table_templete(
  subid int COMMENT '这是注释',
  peerid string COMMENT '这是注释',
  movieid int)
partitioned by (ds string)
row format delimited
lines terminated by '\n'
fields terminated by '\t' -- 或者其他';'
collection items terminated by ','
map keys terminated by ":" 
stored as textfile;
```

内部表

```mysql
use kankan_odl;drop table if exists hive_table_templete;
create table if not exists hive_table_templete(
  subid int,
  peerid string,
  movieid int)
partitioned by (ds string)
row format delimited
lines terminated by '\n'
fields terminated by '\t'
collection items terminated by ','
map keys terminated by ":" 
stored as textfile;
```

> 只有文本存储格式才能使用`load data local inpath`的方法进行数据加载填充

###### 序列化格式

```sql
use kankan_odl;drop table if exists hive_table_templete;
create external table if not exists union_install(
   Fu1 string,
   Fu2 string,
   Fu8 string,
   Fu9 string,
   Fip string,
   Finsert_time int,
   isp string
  )
partitioned by (ds string,hour string)
row format delimited
lines terminated by '\n'
fields terminated by '\u0001'
stored as inputformat
  'org.apache.hadoop.mapred.SequenceFileInputFormat'
outputformat
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat';
```
```mysql
use xmp_data_mid;
drop table if exists guid_action;
create table if not exists guid_action(
   guid string,
   flag1 string,
   flag2 string,
   flag3 string,
   num	int
  )
partitioned by (dyear string,dmon string)
row format delimited
fields terminated by '\t';
```

```mysql
CREATE TABLE `odl_xxx_android_sdk_action_info`(
  `appid` string, 
  `interid` string, 
  `eventid` string, 
  `oprtime` string, 
  `extdata` map<string,string>)
PARTITIONED BY ( 
  `day` string, 
  `hour` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'colelction.delim'=',', 
  'field.delim'='\t', 
  'mapkey.delim'='=', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.SequenceFileInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat'
LOCATION
  'hdfs://wh-ns/user/complat/warehouse/xxxx_sdk_odl.db/odl_xxxxx_android_sdk_action_info';
```

##### 查看表

```shell
# 按正条件（正则表达式）显示表，
SHOW TABLES '.*s';
```

###### 表结构

```shell
#方法1：查看表的字段信息
desc table_name;

#方法2：查看表的字段信息及元数据存储路径
desc extended table_name;

#方法3：查看表的字段信息及元数据存储路径
desc formatted table_name;

#方法4：查看建表语句及其他详细信息的方法
show create table table_name;
```

###### 表容量

```shell
hadoop fs -ls xxxx |awk -F ' ' '{print $5}'|awk '{a+=$1}END{print a/(1024*1024*1024)}'  # 单位G
```

##### 创建视图

视图是只读的，不能向视图中插入或是加载数据，视图可以被定义为多个表的连接，也可以被定义为只有部分列可见，也可为部分行可见。

- 视图的优点：

​                首先，可以简化数据查询语句

​                其次，可以使用用户能从多角度看待同一数据

​                然后，通过引入视图可以提高数据的安全性

​                最后，视图提提供了一定程度的逻辑独立性等。

- 引入视图机制带来的好处：

​        通过引入视图机制，用户可以将注意力集中在其关心的数据上（而非全部数据），这样就大大提高了用户效率与用户满意度，而且如果这些数据来源于多个基本表结构，或者数据不仅来自于基本表结构，还有一部分数据来源于其他视图，并且搜索条件又比较复杂时，需要编写的查询语句就会比较烦琐，此时定义视图就可以使数据的查询语句变得简单可行。

​       定义视图可以将表与表之间的复杂的操作连接和搜索条件对用户不可见，用户只需要简单地对一个视图进行查询即可，故增加了数据的安全性，但不能提高查询效率。

```mysql
create view v_highfun_test as select day,cookieid from highfun_test;
```

##### 查看视图

```mysql
select * from v_highfun_test;
```

####  属性修改

##### 分区操作

###### 显示分区

```mysql
use xmp_odl;show partitions $tbl partition(ds='$date');
```

###### 添加分区

```mysql
use xmp_odl;alter table $tbl add if not exists partition (ds='$date',hour='$hour');

# 此外也可以通过insert进行插入创建
insert overwrite table xxx partition(ds=xxx);
insert into  table xxx partition(ds=xx);
```

> 使用insert into插入的时候需要指定所有的分区，不然提示失败

[动态分区和静态分区](http://www.aboutyun.com/home.php?mod=space&uid=1415&do=blog&quickforward=1&id=3093)

```
#动态分区和静分区的区别
```

###### 删除分区

```mysql
use xmp_odl;
alter table $tbl drop if exists partition(ds='20160808',hour='00');

#例子
alter table odl_shoulei_adv_gdtinfo drop if exists partition (ds='$date');

# 若分区下存在子分区，则连子分区一起删除
hive> alter table guid_action drop if exists partition(dtask='meizu');
Dropped the partition dtask=meizu/dyear=2017/dmon=201703
Dropped the partition dtask=meizu/dyear=2017/dmon=201704
Dropped the partition dtask=meizu/dyear=2017/dmon=201705
Dropped the partition dtask=meizu/dyear=2017/dmon=201706
```

> 问题：为什么在insert overwrite table之前一般都先使用这个语句删除对应的分区

###### 修改分区

```sql
# 修改分区位置
alter table $tbl partition(ds='20160808',hour='00') set location "/user/kankan/warehouse/..."

# 修改分区名
alter table $tbl partition(ds='20160808',hour='00') rename to partition(ds='20160808',hour='01')
```

==分区综合例子：==

动态分区：

```mysql
alter table xxx drop if exists partition (ds='$date');
insert overwrite table xxx partition(ds='${date}',appid,servid)
select 
	,other
	,appid
	,serverid
from 
	vvvv;
# 运行的时候会根据appid、serverid的不同值自动进入相应的分区中
```

> 但要注
>
> ```shell
> Dynamic partition cannot be the parent of a static partition ''xsdnerrcode'';
> ```
>
> 

##### 字段操作

###### 添加列

```mysql
alter table $tbl add columns(col_name string comment 'this is comment');
```

> 注意hive不支持直接添加列到指定位置，解决方案是先添加列，然后再修改列到指定的位置
>
> ```mysql
> alter table $tbl change col_name newcol_name string [after x][first];
> ```

添加列并设置为分区列：

```mysql
# 暂时没有找到解决的办法
```

###### 修改列

```mysql
alter table $tbl change col_name newcol_name string [after x][first];
#在修改列名的过程中可以改变列的位置
```

###### 删除列

```mysql
alter table $tbl drop [column] column_name;
```

> 备注：使用此种方法并不能删除列，具体的列删除方法[参考](https://stackoverflow.com/questions/34198114/alter-hive-table-add-or-drop-column),只能使用列替换的方式进行删除
>
> ```mysql
> ALTER TABLE emp REPLACE COLUMNS( name string, dept string);
> ```

###### 替换列

```mysql
alter table name replace columns (col_spec[, col_spec ...]);
```

##### 表操作

参数设置,修改，存储格式，分桶

###### 表重命名

````mysql
use xmp_odl;alter table $tbl rename to new_tbl_name;
````

###### 修改表存储属性

```sql
# 修改存储格式
alter TABLE  pusherdc   SET FILEFORMAT
INPUTFORMAT "org.apache.hadoop.mapred.SequenceFileInputFormat"
OUTPUTFORMAT "org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat";


# 修改字段分割方式
alter table xmp_subproduct_install set SERDEPROPERTIES('field.delim' = '\u0001');
alter table xmp_subproduct_install set SERDEPROPERTIES('serialization.format' = '\u0001');
```

###### 删除表

对外部表（存储在本地文件系统）和内部表（存储在MetaStore），删除语句相同

```shell
drop table if exists $tbl;
```

> 删除的时候会连分区和文件(内部表)一起删除

删除表的部分分区

```shell
alter table dog drop partition(sex='boy');
```

### 查询

#### 基本

> 不嵌套，只使用最基本的，无连接，主要是注意积累函数的使用

##### case when 

case when ..  then  .. else  .. end as ..

两种用法

```mysql
# 方式1
case fruit
  when 'apple' then 'the owner is apple'
  when 'orange' then 'the owner is orange'
  else 'it is another fruit'
end

# 方式2
case 
  when fruit = 'apple' then 'the owner is apple'
  when fruit = 'orange' then 'the owner is orange'
  else 'it is another fruit'
end
```

例子1：

```mysql
select fu5[2],
      (case
          when(fu2[1]=0) then '0'
          when(fu2[1]>0 and fu2[1]<=10) then '1'
          when(fu2[1]>10 and fu2[1]<=20) then '2'
          when(fu2[1]>20 and fu2[1]<=60) then '6'
          when(fu2[1]>60 and fu2[1]<=300) then '300'
          when(fu2[1]>300 and fu2[1]<=7200) then '7200'
          else '-1'
      end) as section,
      fu6
from xmpplaydur 
where size(fu5)!=0 and fu5[0]>=1023；
```

例子2：

```mysql
select 
	case when (fu6>=0 and fu6<1024) then '[0,1)' 
		when (fu6>=1024 and fu6<2048) then '[1,3)' 
		when (fu6>=2048 and fu5<3072) then '[2,3)' 
		when (fu6>=3072 and fu6<4096) then '[3,4)' 
		when fu6>=4096 then '[4,)' 
		else 'error' 
		end as 'dur',
	if((lower(fu7) regexp "geforce") ,'yes','no'),
	count(*) 
from xmp_odl.xmpcloud2 
where ds='20170618' and fu3='2341' and fu2 in (3,4,5) 
group by substr(fu6,1,1),if((lower(fu7) regexp "geforce"),'yes','no') 
order by tsize limit 10;
```

##### coalesce

COALESCE( value1,value2,... )

The COALESCE function returns the fist not NULL value from the list of values. If all the values in the list are NULL, then it returns NULL.

```mysql
select COALESCE(NULL,1,"ww") from test.dual;
# coalesce能否返回数组中第一个非NULL的？

```

> 如何返回数组中的第一个非NULL元素，配合collect_list使用？取聚合后第一个非空元素
>
> ```mysql
> (case when sort_array(collect_set(version))[0]='' and size(collect_set(version))=1 then ''
>       when sort_array(collect_set(version))[0]!='' then sort_array(collect_set(version))[0]
>       when sort_array(collect_set(version))[0]='' and size(collect_set(version))>1 then 			   collect_set(version)[1] end
> ) as version
> ```

#### 子查询

子查询要和连接一起学习

```mysql
SELECT
	a.mt,
	count(*) AS cnt
FROM
	(
		SELECT
			from_unixtime(finsert_time,'yyyyMMdd HH:mm:ss') AS mt
		FROM
			xmp_odl.xmp_pv
		WHERE
			ds = '20161206'
	) a
GROUP BY
	a.mt
ORDER BY
	cnt DESC;
```

#### 正则

##### 元字符

hive中的正则转义使用两个反斜杠， 即‘//’，

基础元字符1：

| 元字符            | 含义                               | 备注   |
| -------------- | -------------------------------- | ---- |
| .              | 任何字符                             |      |
| ?              | a?表示a出现一次或一次也没有                  | 扩展正则 |
| *              | a*表示a出现零次或多次                     |      |
| +              | a+表示a出现一次或多次                     | 扩展正则 |
| {n}            | a{n}表示a恰好出现n次                    |      |
| a{n,}          | a{n，}表示a至少出现n次                   |      |
| a{n,m}         | a{n,m}表示a至少出现n次，不超过m次            |      |
| \|             | 两者取其一：Java\|Hello 表示  Java或Hello | 扩展正则 |
| []             | [abc]表示a或b或c                     |      |
| [^]            | [^abc]表示除了a、b、c、以外的字符            |      |
| [a-zA-Z]       | 表示任何大小写字符                        |      |
| [a-d[m-p]]     | 表示a到d或m-p的字符；并集                  |      |
| [a-z&&[def]]   | d、e  或 f（交集）                     |      |
| [a-z&&\[^bc]]  | a 到  z，除了  b 和  c：[ad-z]（减去）     |      |
| [a-z&&\[^m-p]] | a 到  z，而非  m 到  p：[a-lq-z]（减去）   |      |
| ^              | 行的开头                             |      |
| $              | 行的结尾                             |      |

基础元字符2：

| 元字符  | 含义                                       | 备注   |
| ---- | ---------------------------------------- | ---- |
| \\d  | 数字：[0-9]                                 |      |
| \\D  | 非数字：  [^0-9]                             |      |
| \\s  | 空白字符                                     |      |
| \\S  | 非空白字符：[^\\s]                             |      |
| \\w  | 单词字符：[a-zA-Z_0-9]                        |      |
| \\W  | 非单词字符：\[^\\w]                            |      |
| (?i) | 这个标志能让表达式忽略大小写进行匹配                       |      |
| (?x) | 在这种模式下，匹配时会忽略(正则表达式里的)空格字符，例如空格，tab，回车之类 |      |

例子：

```shell
vsw rlike '^.*(share_result|zan|discuss_result|follow_click_result|transmit_result)$';
```

##### 正则匹配

```mysql
# 正则匹配
select  'abc'  regexp '^[a-z]*$'   from test.dual;
select  'http://v.xunlei.com'  regexp 'http://v.xunlei.com/?$'   from test.dual; #true

select 'www.eee23232.com' rlike 'www.(eee[0-9]{2,}|fff[0-9]{2,}).com' from test.dual;
```

##### [正则抽取](http://blog.csdn.net/jv_rookie/article/details/55211955)

```mysql
# 正则抽取（注意此处不能使用\d和\w等类似的字符）
select regexp_extract('http://xxx/details/0/40.shtml','http://xxx/details/([0-9]{1,})/([0-9]{1,})\.shtml',1) from test.dual; # 返回40

select regexp_extract('5.2.14.5672',"(^\\d+)\\.(\\d+)\\.(\\d+)",0); 
select regexp_extract('0796-7894145','(^\\d{3,4})\\-?(\\d{7,8}$)',1); //结果0796
select regexp_extract('https://pay.xunlei.com/bjvip.html?referfrom=v_pc_xl9_push_noti_nfxf','(.*)\\?referfrom=(.*)',1); //结果https://pay.xunlei.com/bjvip.html
```

> 正则抽取中的贪婪匹配
>
> ```mysql
> # 提取某个分割符中的最后一位
> select regexp_extract('a,b,c,de,f2g2','(.*),(.*)',2); 
>
> #提取中文标题的尝试
> select regexp_extract('D:\迅雷下载\[2015]小森林小森林\夏秋篇.Little.Forest.Summer.Autumn.rmvb_snapshot_00[2015.08.31_09].jpg','(.*)\(.*)',1);  #提取路径
> select regexp_extract(filename,'(.*)/(.*)',2);  # 提取文件名
>
> select regexp_extract('x=123abcde&x=18456abc&x=2&y=3&x=4','x=([0-9]+)([a-z]+)',2);
> ```
>

例子：

```mysql
# 提取中文字字符
select regexp_extract(results,'([\\u4e00-\\u9fa5]+)',1) from vip_mid.vip_block_detail_djq_d limit 3;
select regexp_extract('dui你ada 大坏2232！ 蛋','([\\u4e00-\\u9fa5]+)',1) from test.dual; #你


# 提取文件后缀(在shell中\\要变成\\\\)
select lower(regexp_extract(xl_urldecode(xl_urldecode(filename)),'(.*)\\.(.*)',2)); -- rmvb
select regexp_extract('zhang.mei.nv.rmvb','(.?)\\.(.*)',2);  -- mei.nv.rmvb  (采用非贪婪模式)
select regexp_extract('zhang.mei.nv.rmvb','(.*)\\.(.*)',2);  -- rmvb  (采用贪婪模式)
```

##### 正则替换

```mysql
# 正则替换
select regexp_replace('foobar','oo|ba','') from test.dual; # 返回fr

# 正则替换特殊字符--命令行版本
select regexp_replace('<李>{二}狗(张)|).%-+&【德! 】*[ 江 ]?','_|\\\|>|<|\\{|\\}|%|\\||!|@|#|$|\\s|\\[|\\]|\\.|\\?|\\*|【|】|，|\\(|\\)|：|&|-|\\+|:|。|','');

# 正则替换特殊字符--shell版
select regexp_replace('<李>{二}狗(张)|).%-+&【德! 】*[ 江 ]?','_|\\\\\\|>|<|\\\\{|\\\\}|%|\\\\||!|@|#|$|\\\\s|\\\\[|\\\\]|\\\\.|\\\\?|\\\\*|【|】|，|\\\\(|\\\\)|：|&|-|\\\\+|:|。|','');
```

例子：

```mysql
# 正则替换获取中文字符
select regexp_replace(results,'([\\w\\:\\;\\"\\.]+)','') from vip_mid.vip_block_detail_djq_d limit 3;
```

##### 正则分割

```mysql
# 正则分割
select split(fu1,'\\.') from xmp_odl.xmpcloud2 where ds='20170502' and hour=11 limit 10;

# 正则非中文字符分割（得到中文字符序列）
select split('张1大2332额都是大坏蛋，！dwe wo们','[^\\u4e00-\\u9fa5]+')[2] from test.dual;
```

一个综合正则例子：

```mysql
# 正则聚合
select substr(fu6,1,1) as tsize,if((lower(fu7) regexp "geforce") ,'yes','no'),count(*) from xmp_odl.xmpcloud2 where ds='20170618' and fu3='2341' and fu2 in (3,4,5) group by substr(fu6,1,1),if(( lower(fu7) regexp "geforce"),'yes','no') order by tsize;

# 提取
http://v.xunlei.com/tv/
http://v.xunlei.com/movie_tuijian/teleplay_tuijian.shtml
http://list.v.xunlei.com/v,type/5,teleplay/
select parse_url('http://list.v.xunlei.com/v,type/5,teleplay/','PATH') from test.dual;
select regexp_extract('http://list.v.xunlei.com/v,type/5,teleplay/','http://list.v.xunlei.com/v,type/5,([a-z]*)/',1) from test.dual; # 返回teleplay

http://v.xunlei.com/zongyi/
http://v.xunlei.com/movie_tuijian/tv_tuijian.shtml
http://list.v.xunlei.com/v,type/5,tv/

http://v.xunlei.com/dongman/
http://v.xunlei.com/movie_tuijian/anime_tuijian.shtml
http://list.v.xunlei.com/v,type/5,anime/

http://v.xunlei.com/movie/
http://v.xunlei.com/movie_tuijian/movie_tuijian.shtml
http://list.v.xunlei.com/v,type/5,movie/

# 文件名分割
select split("A:\xunlei\白石\0502star777\宣傳文件\魔王之家~魔王在線防屏蔽發布器.rar",'\\\\') from test.dual;
select split(r"A:\xun\白石\大哥\wzhang\vvv.rar",'\\\') from test.dual;
```

####  连接

连接是在查询中最广泛使用的，但要注意数据倾斜问题,==而且join中on的字段不能放在where中==

##### left [outer] join

left join(左连接)：返回两个表中连结字段相等的行和左表中的行；

>  左表(A)的记录将会全部表示出来,而右表(B)只会显示符合搜索条件的记录(例子中为: A.aID = B.bID),B表记录不足的地方均为NULL.

```mysql
insert overwrite table download_union.register_web_all partition(dt='$dt',stat_source='tel') 
select utmp.mac, utmp.userdetails, utmp.createdtime, utmp.productflag 
from (
	select t1.mac, t1.userdetails, t1.createdtime, t1.productflag from 
    
    (select concat(substring(peerid,0,12),'0000') as mac, userdetails, createdtime, productflag from dbl.tb1 t where t.ds='$dt' and fproduct_type='web' and fisp='tel') t1 
	
    left outer join  
   
   (select concat(substring(peerid,0,12),'0000') as mac, userdetails, createdtime, productflag from db2.tb2 where stat_source='tel' ) t2 
	
    on (t1.mac = t2.mac) 
	where t2.mac is null or t2.mac=null
) utmp;

# 解读：
# 其中utmp表是t1表和t2表关联的结果（t1表和t2进行左连接，连接条件是两个表的mac地址相等，且t2的mac地址为空）
# 其中t1表结果来自dbl.tb1，t2表结果来自db2.tb2
```

##### right [outer] join

right join(右连接)：返回包括右表中的所有记录和左表中连接字段相等的记录。

> right outer join的结果刚好相反,这次是以右表(B)为基础的,A表不足的地方用NULL填充.

```mysql

```

##### full [outer] join

全外连接

```mysql

```

##### inner join

inner join(等值连接)：只返回两个表中连接字段相等的行, `inner join` 有时简写为`join`

```mysql
SELECT
	persons.lastname,
	persons.firstname,
	orders.orderno
FROM
	persons
INNER JOIN orders 
ON persons.id_p = orders.id_p
WHERE
	perssons.lastname LIKE '%小狗%'
ORDER BY
	persons.lastname;
```

例子：求交集

```mysql
select count(distinct a.pid)
from
(
  select pid 
  from xmp_bdl.xmp_dau
  where ds>='20170701' and ds<='20170731' and version<=5619
)a 
join
(
  select peerid
  from thunder9_bdl.bl_xl9_user_accum
  where ds='20170731' and last_active_date>='20170701' and last_active_date<='20170731'
)b
on a.pid=b.peerid;
```

##### map join

​	mapjoin会把小表全部读入内存中，在map阶段直接拿另外一个表的数据和内存中表的数据做匹配，而普通的equality join则是类似于mapreduce中的filejoin,需要先分组，然后在reduce端进行连接，由于mapjoin是在map是进行了join操作，省去了reduce的运行，效率也会高很多

​	mapjoin还有一个很大的好处是能够进行不等连接的join操作，如果将不等条件写在where中，那么mapreduce过程中会进行笛卡尔积，运行效率特别低，这是由于equality join （不等值join操作有 >、<、like等如：a.x < b.y 或者 a.x like b.y） 需要在reduce端进行不等值判断，map端只能过滤掉where中等值连接时候的条件，如果使用mapjoin操作，在map的过程中就完成了不等值的join操作，效率会高很多。

```mysql
select A.a ,A.b from A join B where A.a>B.a
```

###### 应用场景

- 关联操作中有一张表非常小
- 不等值的连接操作

例子：

```mysql
select t1.a,t1.b from table t1 join table2 t2  on ( t1.a=t2.a and t1.datecol=20110802)

# 改进后
select /*+ mapjoin(t1)*/ t1.a,t1.b from table t1 join table2 t2  on ( t1.a=t2.a and f.ftime=20110802) 
```

> 该语句中t2表有30亿行记录，t1表只有100行记录，而且t2表中数据倾斜特别严重，有一个key上有15亿行记录，在运行过程中特别的慢，而且在reduece的过程中遇有内存不够而报错

###### 进阶

连接小表的时候，在内存中操作，省去reduce过程,和common join存在着差别

```mysql
#设置参数：
set hive.auto.convert.join=true;
set hive.mapjoin.smalltable.filesize=250000
```

使用样例：

```mysql
select /*+ MAPJOIN(A) */ 字段
from 小表 A
right outer join 大表 B
on A.XX=B.XX
```

##### muti join

多表join , 优化代码结构

```mysql
select .. from join tables (a,b,c) with keys (a.key, b.key, c.key) where ....   
```

关联条件相同多表join会优化成一个job

##### left semi join

[left semi join](https://blog.csdn.net/wisdom_c_1010/article/details/78774129)是可以高效实现in/exists子查询的语义，

- 当A表中的记录，在B表上产生符合条件之后就返回，不会再继续查找B表记录了
- select的只能是左侧表的字段，不能出现右侧表的字段
- 不支持在on条件中使用in ()

```mysql
 select a.key,a.value from a where a.key in (select b.key from b);
（1）未实现left semi-join之前，hive实现上述语义的语句是：
   select t1.key, t1.value from a t1
   left outer join (select distinctkey from b) t2 
   on t1.id = t2.id
   where t2.id is not null;

（2）可被替换为left semi join如下：
   select a.key, a.val from a left semi join b on (a.key = b.key)
   这一实现减少至少1次mr过程，注意left semi-join的join条件必须是等值。
```

例子：

```mysql
select a.guid,a.eventid from xlj_test_event a left semi join xlj_test_user b on a.guid=b.guid and a.ds=20150527 and b.ds=20150527 and a.eventid=3604 limit 40;

select a.pid,b.flag from xmp_mid.dau_pid a left semi join xmp_bdl.xmp_kpi_active b  on (a.pid=b.pid) where a.minds=20160101 and b.ds=20160109 limit 10;
```

==join中的on和where执行顺序==

```mysql
# inner join中on和where的顺序对执行结果无影响
select * form tab1 left join tab2 on (tab1.size = tab2.size and tab2.name='AAA');# 在on中判断
```

![on和where顺序](http://tuling56.site/imgbed/2018-07-13_163312.png)

#### 分组

##### grouping sets

```mysql
group by a,b,c
grouping sets ((),(a,b,c),(a,c))
```

##### with cube

```mysql
group by xx1,xx2,xx3
with cube

# 其等效于
group by xx1,xx2,xx3
grouping sets((),(xx1),(xx1,xx2),(xx1,xx2,xx3));
```

### 函数

#### 库函数

##### 字符串

字符串处理函数一览

| 返回类型                         | 函数名                                      | 描述                                       |
| ---------------------------- | ---------------------------------------- | ---------------------------------------- |
| int                          | ascii(string str)                        | 返回str第一个字符串的数值                           |
| string                       | base64(binary bin)                       | 将二进制参数转换为base64字符串                       |
| string                       | concat(string\|binary A, string\|binary B...) | 返回将A和B按顺序连接在一起的字符串，如：concat('foo', 'bar') 返回'foobar' |
| array<struct<string,double>> | context_ngrams(array<array<string>>, array<string>, int K, int pf) | 从一组标记化的句子中返回前k个文本                        |
| string                       | concat_ws(string SEP, string A, string B...) | 类似concat() ，但使用自定义的分隔符SEP                |
| string                       | concat_ws(string SEP, array<string>)     | 类似concat_ws() ，但参数为字符串数组                 |
| string                       | decode(binary bin, string charset)       | 使用指定的字符集将第一个参数解码为字符串，如果任何一个参数为null，返回null。可选字符集为： 'US_ASCII', 'ISO-8859-1', 'UTF-8', 'UTF-16BE', 'UTF-16LE', 'UTF-16' |
| binary                       | encode(string src, string charset)       | 使用指定的字符集将第一个参数编码为binary ，如果任一参数为null，返回null |
| int                          | find_in_set(string str, string strList)  | 返回str在strList中第一次出现的位置，strList为用逗号分隔的字符串，如果str包含逗号则返回0，若任何参数为null，返回null。如： find_in_set('ab', 'abc,b,ab,c,def') 返回3 |
| string                       | format_number(number x, int d)           | 将数字x格式化为'#,###,###.##'，四舍五入为d位小数位，将结果做为字符串返回。如果d=0，结果不包含小数点或小数部分 |
| string                       | get_json_object(string json_string, string path) | 从基于json path的json字符串中提取json对象，返回json对象的json字符串，如果输入的json字符串无效返回null。Json 路径只能有数字、字母和下划线，不允许大写和其它特殊字符 |
| boolean                      | in_file(string str, string filename)     | 如果str在filename中以正行的方式出现，返回true           |
| int                          | instr(string str, string substr)         | 返回substr在str中第一次出现的位置。若任何参数为null返回null，若substr不在str中返回0。Str中第一个字符的位置为1 |
| int                          | length(string A)                         | 返回A的长度                                   |
| int                          | locate(string substr, string str[, int pos]) | 返回substr在str的位置pos后第一次出现的位置              |
| string                       | lower(string A) lcase(string A)          | 返回字符串的小写形式                               |
| string                       | lpad(string str, int len, string pad)    | 将str左侧用字符串pad填充，长度为len                   |
| string                       | ltrim(string A)                          | 去掉字符串A左侧的空格，如：ltrim(' foobar ')的结果为'foobar ' |
| array<struct<string,double>> | ngrams(array<array<string>>, int N, int K, int pf) | 从一组标记化的Returns the top-k 句子中返回前K个N-grams |
| string                       | parse_url(string urlString, string partToExtract [, string keyToExtract]) | 返回给定URL的指定部分，partToExtract的有效值包括HOST，PATH， QUERY， REF， PROTOCOL， AUTHORITY，FILE和USERINFO。例如：  parse_url('http://facebook.com/path1/p.php?k1=v1&k2=v2#Ref1', 'HOST') 返回 'facebook.com'.。当第二个参数为QUERY时，可以使用第三个参数提取特定参数的值，例如： parse_url('http://facebook.com/path1/p.php?k1=v1&k2=v2#Ref1','QUERY', 'k1') 返回'v1' |
| string                       | printf(String format, Obj... args)       | 将输入参数进行格式化输出                             |
| string                       | regexp_extract(string subject, string pattern, int index) | 使用pattern从给定字符串中提取字符串。如： regexp_extract('foothebar', 'foo(.*?)(bar)', 2) 返回'bar' 有时需要使用预定义的字符类：使用'\s' 做为第二个参数将匹配s，'s'匹配空格等。参数index是Java正则匹配器方法group()方法中的索引 |
| string                       | regexp_replace(string INITIAL_STRING, string PATTERN, string REPLACEMENT) | 使用REPLACEMENT替换字符串INITIAL_STRING中匹配PATTERN的子串，例如： regexp_replace("foobar", "oo\|ar", "") 返回'fb' |
| string                       | repeat(string str, int n)                | 将str重复n次                                 |
| string                       | reverse(string A)                        | 将字符串A翻转                                  |
| string                       | rpad(string str, int len, string pad)    | 在str的右侧使用pad填充至长度len                     |
| string                       | rtrim(string A)                          | 去掉字符串A右侧的空格，如： rtrim(' foobar ') 返回 ' foobar' |
| array<array<string>>         | sentences(string str, string lang, string locale) | 将自然语言文本处理为单词和句子，每个句子在适当的边界分割，返回单词的数组。参数lang和local为可选参数，例如： sentences('Hello there! How are you?') 返回( ("Hello", "there"), ("How", "are", "you") ) |
| string                       | space(int n)                             | 返回n个空格的字符串                               |
| array                        | split(string str, string pat)            | 用pat分割字符串str，pat为正则表达式                   |
| map<string,string>           | str_to_map(text[, delimiter1, delimiter2]) | 使用两个分隔符将文本分割为键值对。第一个分隔符将文本分割为K-V 对，第二个分隔符分隔每个K-V 对。默认第一个分隔符为“**，**“，第二个分隔符为= |
| string                       | substr(string\|binary A, int start) substring(string\|binary A, int start) | 返回A从位置start直到结尾的子串                       |
| string                       | substr(string\|binary A, int start, int len) substring(string\|binary A, int start, int len) | 返回A中从位置start开始，长度为len的子串，如： substr('foobar', 4, 1) 返回 'b' |
| string                       | translate(string input, string from, string to) | 将input中出现在from中的字符替换为to中的字符串，如果任何参数为null，结果为null |
| string                       | trim(string A)                           | 去掉字符串A两端的空格                              |
| binary                       | unbase64(string str)                     | 将base64字符串转换为二进制                         |
| string                       | upper(string A) ucase(string A)          | 返回字符串A的大写形式                              |

额外函数

| 函数             | 用法                           | 备注   |
| -------------- | ---------------------------- | ---- |
| xl_md5('aacw') | Returns the md5 value of str |      |
|                |                              |      |
|                |                              |      |

一般函数

```mysql
（1）length(stringA)：返回字符串长度

（2）concat(stringA, string B...)：
     合并字符串，例如concat('foo','bar')='foobar'。注意这一函数可以接受任意个数的参数

（3）substr(stringA, int start) substring(string A,int start)：
     返回子串，例如substr('foobar',4)='bar'
	 倒数第一位substr(xxx,-1)
	 倒数第二位substr(substr(xxx,-2),1,1)

（4）substring(string A, int start,int len)：
     返回限定长度的子串，例如substr('foobar',4, 1)='b'

（5）split(stringstr, string pat)：
     返回使用pat作为正则表达式分割str字符串的列表。例如，split('foobar','o')[2] = 'bar'。

（6）getkeyvalue(str,param) # 自定义
     从字符串中获得指定 key 的 value 值 UDFKeyValue
     CREATE TEMPORARY FUNCTION getkeyvalue  AS 'com.taobao.hive.udf.UDFKeyValue';

（7）instr(string a,sting b)
	#截取某个字符后面的所有字符
	select substring('a=bc.=d=ahhw&e=12',instr('a=bc.=d=ahhw&e=12','d='));
	# 类似实现(取前后匹配的)
	select regexp_extract('a=bc.=d=ahhw&e=12','(.*)d=(.*)',2);
```

字符串分割

```mysql
# 一般字符
select split('a,b,c,d',',')[0] from test.dual;

# 特殊字符
select split('192.168.0.1','\\.') from test.dual; -- 也可以是 split('192.168.0.1','\\\.') 
-- 在shell中split(cv,'\\\.')或者split(cv,'\\\\.'),经转化后是split(cv,'\\.')

# 分号分隔符的处理
select split(xl_urldecode(xl_urldecode(extdata_map['contentlist'])),'\073');　-- 在语句中xx.hql可用
select split('192;168;0;1','\\;') from test.dual; -- 在命令行中不可用

# 分割取最后一个
select reverse(split(reverse('a1,b1,c1,d2'),',')[0]);

# 在shell脚本或者“”内
当然当split包含在 "" 之中时 需要加4个\，如 
hive -e "select split('192.168.0.1','\\\\.')"  不然得到的值是null


# 字符串分割后得到数组中的最后一个(主要用来提取全路径中的文件名)
# windows系统
select split(x.filename,'\\\\\\\\')[x.cnt-1] as fname 
from(
       select filename,size(split(uridecode(filename),'\\\\\\\')) as cnt from  tt
)x

# linux系统
select split(x.filename,'\\/')[x.cnt-1] as fname 
from(
       select filename,size(split(uridecode(filename),'\\/')) as cnt from  tt
)x
                                  
```

> 注意：
>
> - 当待分割的字符串是空或者null的时候，使用size(split('cw3ew3','xx'))得到的数组长度却是1，可通过以下方式修正：select if(length('')==0,0,size(split('','_'))) from test.dual;
>
> - 当[分割符号是‘;’号](http://blog.csdn.net/dj_2009291007/article/details/78667695)的时候，因为分号是sql的结束符，在HDFS中识别不了，因此需要用分号的二进制`\073`来表示
>
>   ```mysql
>   select
>     totalprice,
>     email 
>   from
>     prd_updated.ecom_ms_order_udl m 
>   lateral view explode(split ( m.p_ccemailaddress,'\073')) adtable as email 
>   where
>     email !=''
>   ```
>
>   ​

字符串截取

```mysql
select substr('123456',0,2) from test.dual; # 其等价于substr('123456',1,2),从0开始和从1开始的结果是相同的
# 获取倒数第二个字符
substr(substr('41252292167998464',-2),1,1); # 结果6
```

字符串替换

```mysql
regexp_replace(string INITIAL_STRING, string PATTERN, string REPLACEMENT)
select regexp_replace("foobar", "oo|ar", "")  from test.dual;
select unhex(regexp_replace('%E4%B8%AD%E5%9B%BD','%','')) from test.dual;
```

字符串抽取

```mysql
regexp_extract(string subject, string pattern, int index)
select regexp_extract('foothebar', 'foo(.*?)(bar)', 1) from test.dual;
```

字符串拼接

```mysql
select concat('foo','bar');
select concat_ws('_',array('1','2','3')); #可以直接拼接数组
select concat_ws('_',collect_list(xxx));
```

##### 数字

函数一览

| **Return Type** | **Name (Signature)**                     | **Description**                          |
| --------------- | ---------------------------------------- | ---------------------------------------- |
| DOUBLE          | round(DOUBLE a)                          | Returns the rounded `BIGINT` value of `a`.**返回对a四舍五入的BIGINT值** |
| DOUBLE          | round(DOUBLE a, INT d)                   | Returns `a` rounded to `d` decimal places.**返回DOUBLE型d的保留n位小数的DOUBLW型的近似值** |
| DOUBLE          | bround(DOUBLE a)                         | Returns the rounded BIGINT value of `a` using HALF_EVEN rounding mode (as of [Hive 1.3.0, 2.0.0](https://issues.apache.org/jira/browse/HIVE-11103)). Also known as Gaussian rounding or bankers' rounding. Example: bround(2.5) = 2, bround(3.5) = 4.**银行家舍入法（1~4：舍，6~9：进，5->前位数是偶：舍，5->前位数是奇：进）** |
| DOUBLE          | bround(DOUBLE a, INT d)                  | Returns `a` rounded to `d` decimal places using HALF_EVEN rounding mode (as of [Hive 1.3.0, 2.0.0](https://issues.apache.org/jira/browse/HIVE-11103)). Example: bround(8.25, 1) = 8.2, bround(8.35, 1) = 8.4.**银行家舍入法,保留d位小数** |
| BIGINT          | floor(DOUBLE a)                          | Returns the maximum `BIGINT` value that is equal to or less than `a`**向下取整，最数轴上最接近要求的值的左边的值  如：6.10->6   -3.4->-4** |
| BIGINT          | ceil(DOUBLE a), ceiling(DOUBLE a)        | Returns the minimum BIGINT value that is equal to or greater than `a`.**求其不小于小给定实数的最小整数如：ceil(6) = ceil(6.1)= ceil(6.9) = 6** |
| DOUBLE          | rand(), rand(INT seed)                   | Returns a random number (that changes from row to row) that is distributed uniformly from 0 to 1. Specifying the seed will make sure the generated random number sequence is deterministic.**每行返回一个DOUBLE型随机数seed是随机因子** |
| DOUBLE          | exp(DOUBLE a), exp(DECIMAL a)            | Returns `ea` where `e` is the base of the natural logarithm. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**返回e的a幂次方， a可为小数** |
| DOUBLE          | ln(DOUBLE a), ln(DECIMAL a)              | Returns the natural logarithm of the argument `a`. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**以自然数为底d的对数，a可为小数** |
| DOUBLE          | log10(DOUBLE a), log10(DECIMAL a)        | Returns the base-10 logarithm of the argument `a`. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**以10为底d的对数，a可为小数** |
| DOUBLE          | log2(DOUBLE a), log2(DECIMAL a)          | Returns the base-2 logarithm of the argument `a`. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**以2为底数d的对数，a可为小数** |
| DOUBLE          | log(DOUBLE base, DOUBLE a)log(DECIMAL base, DECIMAL a) | Returns the base-`base` logarithm of the argument `a`. Decimal versions added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**以base为底的对数，base 与 a都是DOUBLE类型** |
| DOUBLE          | pow(DOUBLE a, DOUBLE p), power(DOUBLE a, DOUBLE p) | Returns `ap`.**计算a的p次幂**                 |
| DOUBLE          | sqrt(DOUBLE a), sqrt(DECIMAL a)          | Returns the square root of `a`. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**计算a的平方根** |
| STRING          | bin(BIGINT a)                            | Returns the number in binary format (see [http://dev.mysql.com/doc/refman/5.0/en/string-functions.html#function_bin](http://dev.mysql.com/doc/refman/5.0/en/string-functions.html#function_bin)).**计算二进制a的STRING类型，a为BIGINT类型** |
| STRING          | hex(BIGINT a) hex(STRING a) hex(BINARY a) | If the argument is an `INT` or `binary`, `hex` returns the number as a `STRING` in hexadecimal format. Otherwise if the number is a `STRING`, it converts each character into its hexadecimal representation and returns the resulting `STRING`. (See[http://dev.mysql.com/doc/refman/5.0/en/string-functions.html#function_hex](http://dev.mysql.com/doc/refman/5.0/en/string-functions.html#function_hex), `BINARY` version as of Hive [0.12.0](https://issues.apache.org/jira/browse/HIVE-2482).)**计算十六进制a的STRING类型，如果a为STRING类型就转换成字符相对应的十六进制** |
| BINARY          | unhex(STRING a)                          | Inverse of hex. Interprets each pair of characters as a hexadecimal number and converts to the byte representation of the number. (`BINARY` version as of Hive [0.12.0](https://issues.apache.org/jira/browse/HIVE-2482), used to return a string.)**hex的逆方法** |
| STRING          | conv(BIGINT num, INT from_base, INT to_base), conv(STRING num, INT from_base, INT to_base) | Converts a number from a given base to another (see [http://dev.mysql.com/doc/refman/5.0/en/mathematical-functions.html#function_conv](http://dev.mysql.com/doc/refman/5.0/en/mathematical-functions.html#function_conv)).**将GIGINT/STRING类型的num从from_base进制转换成to_base进制** |
| DOUBLE          | abs(DOUBLE a)                            | Returns the absolute value.**计算a的绝对值**   |
| INT or DOUBLE   | pmod(INT a, INT b), pmod(DOUBLE a, DOUBLE b) | Returns the positive value of `a mod b`.**a对b取模** |
| DOUBLE          | sin(DOUBLE a), sin(DECIMAL a)            | Returns the sine of `a` (`a` is in radians). Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**求a的正弦值** |
| DOUBLE          | asin(DOUBLE a), asin(DECIMAL a)          | Returns the arc sin of `a` if -1<=a<=1 or NULL otherwise. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**求d的反正弦值** |
| DOUBLE          | cos(DOUBLE a), cos(DECIMAL a)            | Returns the cosine of `a` (`a` is in radians). Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**求余弦值** |
| DOUBLE          | acos(DOUBLE a), acos(DECIMAL a)          | Returns the arccosine of `a` if -1<=a<=1 or NULL otherwise. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**求反余弦值** |
| DOUBLE          | tan(DOUBLE a), tan(DECIMAL a)            | Returns the tangent of `a` (`a` is in radians). Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**求正切值** |
| DOUBLE          | atan(DOUBLE a), atan(DECIMAL a)          | Returns the arctangent of `a`. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**求反正切值** |
| DOUBLE          | degrees(DOUBLE a), degrees(DECIMAL a)    | Converts value of `a` from radians to degrees. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6385).**奖弧度值转换角度值** |
| DOUBLE          | radians(DOUBLE a), radians(DOUBLE a)     | Converts value of `a` from degrees to radians. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6327).**将角度值转换成弧度值** |
| INT or DOUBLE   | positive(INT a), positive(DOUBLE a)      | Returns `a`.**返回a**                      |
| INT or DOUBLE   | negative(INT a), negative(DOUBLE a)      | Returns `-a`.**返回a的相反数**                 |
| DOUBLE or INT   | sign(DOUBLE a), sign(DECIMAL a)          | Returns the sign of `a` as '1.0' (if `a` is positive) or '-1.0' (if `a` is negative), '0.0' otherwise. The decimal version returns INT instead of DOUBLE. Decimal version added in [Hive 0.13.0](https://issues.apache.org/jira/browse/HIVE-6246).**如果a是正数则返回1.0，是负数则返回-1.0，否则返回0.0** |
| DOUBLE          | e()                                      | Returns the value of `e`.**数学常数e**       |
| DOUBLE          | pi()                                     | Returns the value of `pi`.**数学常数pi**     |
| BIGINT          | factorial(INT a)                         | Returns the factorial of `a` (as of Hive [1.2.0](https://issues.apache.org/jira/browse/HIVE-9857)). Valid `a` is [0..20].**求a的阶乘** |
| DOUBLE          | cbrt(DOUBLE a)                           | Returns the cube root of `a` double value (as of Hive [1.2.0](https://issues.apache.org/jira/browse/HIVE-9858)).**求a的立方根** |
| INT BIGINT      | shiftleft(TINYINT\|SMALLINT\|INT a, INT b)shiftleft(BIGINT a, INT b) | Bitwise left shift (as of Hive [1.2.0](https://issues.apache.org/jira/browse/HIVE-9859)). Shifts `a` `b` positions to the left.Returns int for tinyint, smallint and int `a`. Returns bigint for bigint `a`.**按位左移** |
| INTBIGINT       | shiftright(TINYINT\|SMALLINT\|INT a, INTb)shiftright(BIGINT a, INT b) | Bitwise right shift (as of Hive [1.2.0](https://issues.apache.org/jira/browse/HIVE-9859)). Shifts `a` `b` positions to the right.Returns int for tinyint, smallint and int `a`. Returns bigint for bigint `a`.**按拉右移** |
| INTBIGINT       | shiftrightunsigned(TINYINT\|SMALLINT\|INTa, INT b),shiftrightunsigned(BIGINT a, INT b) | Bitwise unsigned right shift (as of Hive [1.2.0](https://issues.apache.org/jira/browse/HIVE-9859)). Shifts `a` `b` positions to the right.Returns int for tinyint, smallint and int `a`. Returns bigint for bigint `a`.**无符号按位右移（<<<）** |
| T               | greatest(T v1, T v2, ...)                | Returns the greatest value of the list of values (as of Hive [1.1.0](https://issues.apache.org/jira/browse/HIVE-9402)). Fixed to return NULL when one or more arguments are NULL, and strict type restriction relaxed, consistent with ">" operator (as of Hive [2.0.0](https://issues.apache.org/jira/browse/HIVE-12082)).**求最大值** |
| T               | least(T v1, T v2, ...)                   | Returns the least value of the list of values (as of Hive [1.1.0](https://issues.apache.org/jira/browse/HIVE-9402)). Fixed to return NULL when one or more arguments are NULL, and strict type restriction relaxed, consistent with "<" operator (as of Hive [2.0.0](https://issues.apache.org/jira/browse/HIVE-12082)).**求最小值** |

##### 日期时间

基本操作

```mysql
# 时间戳转日期
select from_unixtime(1527680835,'yyyyMMdd HH:mm:ss') from xmp_odl.xmp_pv where ds='20161206';

# 日期转时间戳
select unix_timestamp('20111207 13:01:03','yyyyMMdd HH:mm:ss') from test.dual;

# 获取日期小时和分
select substr('2011-12-07 13:01:03',1,16) from test.dual;  #2011-12-07 13:01

# 获取小时和分
select substr('2011-12-07 13:01:03',12,5) from test.dual;  #13:01


# 获取小时
select hour('2011-12-07 13:01:03'); # 注意必须是此种格式
select hour(from_unixtime(cast(ts as bigint),'yyyy-MM-dd HH:mm:ss'));


# 统计小时内的最高值
select hour(ftime),count(distinct fpeerid) cnt from xmp_odl.t_stat_play where ds='20170708' group by hour(ftime) order by cnt desc;

# 统计五分钟的最高值
select collect_set(substr(ftime,1,16))[0],int((hour(ftime)*60+minute(ftime))/5),count(distinct fpeerid) cnt from xmp_odl.t_stat_play where ds='20170908' group by int((hour(ftime)*60+minute(ftime))/5) order by cnt desc;

# 统计每10秒内的最高值
select collect_set(ftime)[0],int((hour(ftime)*3600+minute(ftime)*60+second(ftime))/10),count(distinct fpeerid) cnt from xmp_odl.t_stat_play where ds='20170908' group by int((hour(ftime)*3600+minute(ftime)*60+second(ftime))/10) order by cnt desc;
```

> hive日期计算精确到毫秒：
>
> 其中t1是10位的时间戳值，即1970-1-1至今的秒，而13位的所谓毫秒的是不可以的。
>
> 对于13位时间戳，需要截取，然后转换成bigint类型，因为from_unixtime类第一个参数只接受bigint类型。例如
>
> ```mysql
> from_unixtime(t1,'yyyy-MM-dd HH:mm:ss')
> select from_unixtime(cast(substring(tistmp,1,10) as bigint),'yyyy-MM-dd HH:mm:ss');
> ```
>
> 秒和毫秒组合：
>
> ```mysql
> # 截取13位的毫秒，转化为秒+毫秒
> select concat(from_unixtime(cast(substr(1524448307222,1,10) as int),'yyyyMMdd HH:mm:ss'),' ',substr(1524448307222,11,3)) as ts;
> ```

日期运算

```shell
（1）datediff(string enddate, stringstartdate)：
     返回enddate和startdate的天数的差，注意日期必须为该格式
     datediff('2009-03-01','2009-02-27') = 2

（2）date_add(stringstartdate, int days)：
     加days天数到startdate，注意日期必须为该格式
     date_add('2008-12-31', 1) ='2009-01-01'

（3）date_sub(stringstartdate, int days)：
     减days天数到startdate，注意日期必须为该格式
     date_sub('2008-12-31', 1) ='2008-12-30'

（4）date_format(date,date_pattern) --字符串转日期
     CREATETEMPORARY FUNCTION date_format AS'com.taobao.hive.udf.UDFDateFormat';
     根据格式串format 格式化日期和时间值date，返回结果串。
     date_format('2010-10-10','yyyy-MM-dd','yyyyMMdd')
     date_format('2010-12-23','yyyyMMdd');

（5）str_to_date(str,format)  # 字符串转日期（自定义）
     将字符串转化为日期函数
	 CREATE TEMPORARY FUNCTION str_to_date AS 'com.taobao.hive.udf.UDFStrToDate';
     str_to_date('09/01/2009','MM/dd/yyyy');
```

参考:[HIVE时间操作函数](http://www.cnblogs.com/moodlxs/p/3370521.html)

##### 数学函数-窗口

窗口函数主要作用：

- 分区排序
- 动态GroupBy
- TopN
- 累计计算
- 层次查询

窗口函数一览：

- lead
- lag
- first_value
- last_value

###### grouping sets

在一个GROUP BY查询中，根据不同的维度组合进行聚合，等价于将不同维度GROUP BY结果集进行UNION ALL

```mysql
select ds,
	nvl(srctbl,'total'),
	nvl(srcdb,'total'),
	sum(datasize)
from 
	xmp_data_mid.group_test
group by ds,srctbl,srcdb
grouping sets ((),(ds,srctbl),(ds,srcdb));
```

```shell
xmp_data_mid.group_test;
ds				srctbl	srcdb			hour 	datasize
2016/12/26      zkusr   pgv3_split_c2   23      0
2016/12/26      zkusr   pgv3_split_c2   12      0
```

> 注:
>
> - grouping sets里的字段不能有计算字段，但可以有extdata['xx']这样的
>
> ```mysql
> select ds,
> 	nvl(srctbl,'total'),
> 	nvl(srcdb,'total'),
> 	sum(datasize)
> from 
> 	xmp_data_mid.group_test
> group by ds,srctbl,srcdb
> grouping sets ((),(ds,srctbl),(ds,srcdb));
> ```
>

###### cube

根据GROUP BY的维度的所有组合进行聚合。

```mysql
SELECT 
  s1 as c,
  s2,
  COUNT(DISTINCT cookieid) AS uv,
  GROUPING__ID 
FROM 
	high_test;
GROUP BY month,day 
WITH CUBE 
ORDER BY GROUPING__ID;

# 等价于
SELECT NULL,NULL,COUNT(DISTINCT s1) AS uv,0 AS GROUPING__ID FROM high_test
UNION ALL 
SELECT month,NULL,COUNT(DISTINCT s1) AS uv,1 AS GROUPING__ID FROM high_test GROUP BY month 
UNION ALL 
SELECT NULL,day,COUNT(DISTINCT s1) AS uv,2 AS GROUPING__ID FROM high_test GROUP BY day
UNION ALL 
SELECT month,day,COUNT(DISTINCT s1) AS uv,3 AS GROUPING__ID FROM high_test GROUP BY month,day
```

> 注意：
>
> 所有组合进行聚合的时候，存在都为null的情况

###### roll up

是CUBE的子集，以最左侧的维度为主，从该维度进行层级聚合

```mysql
SELECT 
	month,
	day,
	COUNT(DISTINCT cookieid) AS uv,
	GROUPING__ID  
FROM 
	high_test
GROUP BY month,day
WITH ROLLUP 
ORDER BY GROUPING__ID;
```

> 注意：
>
> 曾经聚合的时候第一行为null

###### [lateral view](http://blog.csdn.net/clerk0324/article/details/58600284)

explode将复杂结构一行拆成多行，然后再用lateral view做各种聚合

![原始数据](http://img.blog.csdn.net/20160716215433196)

```mysql
# 简单展开
SELECT pageid, adid
FROM pageAds 
LATERAL VIEW explode(adid_list) adTable AS adid;
```

![转行数据](http://img.blog.csdn.net/20160716215520353)

```mysql
#展开的基础上做聚合
SELECT adid, count(1)
FROM pageAds 
LATERAL VIEW explode(adid_list) adTable AS adid
GROUP BY adid;
```

![展开之后聚合](http://img.blog.csdn.net/20160716215731495)

###### explode

explode就是将hive一行中复杂的array或者map结构拆分成多行

```mysql
# 单列展开
select explode(a) from array_test;
select explode(mymap) as (mymapkey, mymapvalue) from mymaptable;

# 列和集合(数组和map)
```

> explode不能和其它列混合使用，例如
>
> ```mysql
> select ds,explode(a) from array_test;
> ```
>
> 若要混合，请使用类似map的操作方式:
>
> ```mysql
> select ds,k
> from 
> 	array_test
> lateral view explode(a)ed as k;
> ```

将一个map类型按k,v展开并和其它列进行组合成行

```mysql
use shoulei_sdk_odl;
select eventid,
    extdata['event_name'],
    ori,
    xl_urldecode(pars) as pars
from
    xxx.xxxxx 
LATERAL VIEW explode(extdata)ed as ori,pars
where day='20180313' and extdata['xxxx']='xxxxx' 
    and eventid in ('published','upload')
    and ori not rlike '^pub|timestamp'
group by
    eventid,
    extdata['event_name'],
    ori,
    pars;
```

例子解析：(还有问题)

```mysql
# 'id=1232354,author_id=123122,url=xxx,isexists=1;id=1232354,author_id=123122,url=xxx,isexists=0'
# 解析出url

select split('id=1232354,author_id=123122,url=xxx,isexists=1;id=1232354,author_id=123122,url=xxx,isexists=0',';') from test.dual;

select 
	ds,
 	substr(guid,-1),
	mkey,
	mvalue,
	count(*),
	count(distinct guid)
from
(
  select 
  	ds,
    guid,
    content_arr
  from
      test.dual
      lateral view explode(split(xl_urldecode(extdata_map['contentlist'],'\\;')) content_arr
   where ds>='20180314' and ds<='20180314' and appid='45'
      	and eventname='android_linkCollect'
        and attribute1='linkCollect_content_show'
)a
laterval view explode(content_arr) as (mkey,mvalue)
group by 
  ds,
  substr(guid,-1),
  mkey,
  mvalue;
 
```

```mysql
#首页短视频曝光按网络类型改进版(曝光次数去重)
select 
    ds
    ,network
    ,count(*)
    ,count(distinct concat(guid,movieid))
from
(select
    ds
    ,extdata_map['pub_network'] as network
    ,guid
    ,str_to_map(ed,',','=')['id'] as movieid
from
    shoulei_bdl.bl_shoulei_event_fact
lateral view explode(split(xl_urldecode(xl_urldecode(extdata_map['contentlist'])),'\073'))et as ed
where ds in('20180506','20180503') and appid='45' and type='video' 
    and ts>0 and guid!='' and guid!='NULL'
    and attribute1='home_collect_content_show'
)t
group by ds,network;
```

##### 数据函数-分析

###### [cume_dist](http://lxw1234.com/archives/2015/04/185.htm)

小于等于当前值的行数/分组内的总行数,也就是分组百分比

```mysql
SELECT 
  dept,
  userid,
  sal,
  CUME_DIST() OVER(ORDER BY sal) AS rn1,
  CUME_DIST() OVER(PARTITION BY dept ORDER BY sal) AS rn2 
FROM 
	xmp_data_mid.lxw1234;
 
# 结果
dept    userid   sal   rn1       rn2 
-------------------------------------------
d1      user1   1000    0.2     0.3333333333333333
d1      user2   2000    0.4     0.6666666666666666
d1      user3   3000    0.6     1.0
d2      user4   4000    0.8     0.5
d2      user5   5000    1.0     1.0
 
#rn1: 没有partition,所有数据均为1组，总行数为5，
#	  第一行：小于等于1000的行数为1，因此，1/5=0.2
#	  第三行：小于等于3000的行数为3，因此，3/5=0.6
#rn2: 按照部门分组，dpet=d1的行数为3,
#     第二行：小于等于2000的行数为2，因此，2/3=0.6666666666666666
```

###### row_number

ROW_NUMBER() 从1开始，按照顺序，生成分组内记录的序列
比如，按照pv降序排列，生成分组内每天的pv名次

```mysql
SELECT 
  cookieid,
  createtime,
  pv,
  ROW_NUMBER() OVER(PARTITION BY cookieid ORDER BY pv desc) AS rn 
FROM highfun_test;

# 结果
cookieid day           pv       rn
------------------------------------------- 
cookie1 2015-04-12      7       1
cookie1 2015-04-11      5       2
cookie1 2015-04-15      4       3
cookie1 2015-04-16      4       4
cookie1 2015-04-13      3       5
cookie1 2015-04-14      2       6
cookie1 2015-04-10      1       7
cookie2 2015-04-15      9       1
cookie2 2015-04-16      7       2
cookie2 2015-04-13      6       3
cookie2 2015-04-12      5       4
cookie2 2015-04-14      3       5
cookie2 2015-04-11      3       6
cookie2 2015-04-10      2       7
```

row number可以用来进行[分组去重](https://blog.csdn.net/yimingsilence/article/details/70140877)

###### [ntile](http://lxw1234.com/archives/2015/04/181.htm)

NTILE(n)，用于将分组数据按照顺序切分成n片，返回当前切片值

```mysql
SELECT 
  cookieid,
  createtime,
  pv,
  NTILE(2) OVER(PARTITION BY cookieid ORDER BY createtime) AS rn1,-- 分组内将数据分成2片
  NTILE(3) OVER(PARTITION BY cookieid ORDER BY createtime) AS rn2, -- 分组内将数据分成3片
  NTILE(4) OVER(ORDER BY createtime) AS rn3  -- 将所有数据分成4片
FROM 
	xmp_data_mid.highfun_test 
ORDER BY cookieid,createtime;
```

###### [percentile](https://www.2cto.com/database/201705/636701.html)

计算分位数的函数percentile和percentile_approx，percentile要求输入的字段必须是int类型的，而percentile_approx则是数值类似型的都可以 ,返回分位点对应的记录值(该记录值不一定在记录中)。

格式

```shell
使用方式为percentile(col, p)、percentile_approx(col, p,B)，p∈(0,1) .返回col列p分位上的值。B用来控制内存消耗的精度,B越大，结果的准确度越高。默认为10,000。实际col中 distinct的值 其中percentile要求输入的字段必须是int类型的，而percentile_approx则是数值类似型的都可以（此处待确认，有问题）
```

方法

```mysql
# 使用格式
percentile_approx(col,array(0.05,0.5,0.95),9999) #或者
percentile_approx(cast(col as double),array(0.05,0.5,0.95),9999)

# 取排位在倒数第5%的数的取值
percentile_approx(grade, 0.95)

select percentile(cast(id as bigint),array(0.25,0.5,0.75)) from high_test;	      # [4.25,7.5,10.75]
select percentile_approx(cast(id as bigint),array(0.25,0.5,0.75)) from high_test; # [3.5,7.0,10.5]


# 扩展(展开成行)
select explode(percentile(cast(id as bigint),array(0.25,0.5,0.75))) from high_test;
```

> 注意使用前要先对要操作的列进行排序，然后可以根据排序确定分位数。

######   xx\_rank()

> rank系列：rank()/dense_rank()/percent_rank()
>
> - RANK() 生成数据项在分组中的排名，排名相等会在名次中留下空位
> - DENSE_RANK() 生成数据项在分组中的排名，排名相等不会在名次中留下空位
> - PERCENT_RANK 分组内当前行的RANK值-1/分组内总行数-1

rank()

```mysql
# rank统计每组前N个
use xmp_data_mid;
SELECT A.ds, A.srctbl, A.srcdb,A.datasize
  FROM (SELECT T.ds,
               T.srctbl,
               T.srcdb,
               T.hour,
               T.datasize,
               RANK() OVER(PARTITION BY T.srctbl ORDER BY T.datasize DESC) RK
          FROM group_test T) A
 WHERE RK < 4;
```

> 注意：不分区排序(整体排序)
>
> ```mysql
> # 排序后抽样挑选
> select 
> 	* 
> from
> (
>     select 
>         play_duration,
>         play_starttime,
>         play_endtime,
>         rank() over (order by play_duration) as rn
>     from 
>         shoulei_bdl.bl_shoulei_play_native 
>     where ds='20180525' and appid='45'
> )a
> where rn%1000=0;
> ```

dense_rank()

```mysql
# dense_rank
SELECT 
  cookieid,
  createtime,
  pv,
  RANK() OVER(PARTITION BY cookieid ORDER BY pv desc) AS rn1,
  DENSE_RANK() OVER(PARTITION BY cookieid ORDER BY pv desc) AS rn2,
  ROW_NUMBER() OVER(PARTITION BY cookieid ORDER BY pv DESC) AS rn3 
FROM 
	xmp_data_mid.highfun_test
WHERE cookieid = 'cookie1';
```

percent_rank()

```mysql
# percent_rank
# PERCENT_RANK 分组内当前行的RANK值-1/分组内总行数-1
SELECT 
 	 dept,
  	 userid,
  	 sal,
  	 PERCENT_RANK() OVER(ORDER BY sal) AS rn1,   -- 总体百分比
 	 RANK() OVER(ORDER BY sal) AS rn11,          -- 总体排行
 	 SUM(1) OVER(PARTITION BY NULL) AS rn12,     -- 分组内总行数
	 PERCENT_RANK() OVER(PARTITION BY dept ORDER BY sal) AS rn2  -- 分组内rank值 
FROM lxw1234;
 
# 结果
dept    userid   sal    rn1    rn11     rn12    rn2
---------------------------------------------------
d1      user1   1000    0.0     1       5       0.0
d1      user2   2000    0.25    2       5       0.5
d1      user3   3000    0.5     3       5       1.0
d2      user4   4000    0.75    4       5       0.0
d2      user5   5000    1.0     5       5       1.0
 
rn1: rn1 = (rn11-1) / (rn12-1) 
	   第一行,(1-1)/(5-1)=0/4=0
	   第二行,(2-1)/(5-1)=1/4=0.25
	   第四行,(4-1)/(5-1)=3/4=0.75
rn2: 按照dept分组，
     dept=d1的总行数为3
     第一行，(1-1)/(3-1)=0
     第三行，(3-1)/(3-1)=1
```

###### [lag/lead](http://lxw1234.com/archives/2015/04/190.htm)

lag

```
LAG(col,n,DEFAULT) 用于统计窗口内往上第n行值,第一个参数为列名，第二个参数为往上第n行（可选，默认为1），第三个参数为默认值（当往上第n行为NULL时候，取默认值，如不指定，则为NULL）
```

```mysql
select guid,
    ts,
    row_number() over (partition by guid order by ts) ts_order1,
    lag(ts,1) over (partition by guid order by ts) ts_order2
from shoulei_bdl.bl_shoulei_event_fact
where ds='20180615' and appid='45' and type='launch' and attribute1='forground'
    and cv='5.60.2.5510'
limit 100;
```

 lead

```
LEAD(col,n,DEFAULT) 用于统计窗口内往下第n行值,第一个参数为列名，第二个参数为往下第n行（可选，默认为1），第三个参数为默认值（当往下第n行为NULL时候，取默认值，如不指定，则为NULL）
```

```mysql

```

###### [first_value/last_value](http://lxw1234.com/archives/2015/04/190.htm)

first_value取分组内排序后，截止到当前行，第一个值,last_value取分组内排序后，截止到当前行，最后一个值

##### 数学函数-混合

- java_method(class,method [,arg1 [,arg2])
- reflect(class,method [,arg1 [,arg2..]])
- hash(a1 [,a2...])



##### 数学函数-累积

计算一定范围内、一定值域内或者一段时间内的累积和以及移动平均值等

```mysql

```


#### UDF

udf和streaming的区别在于udf必须是在hadoop平台上的文件，而streaming要求的则是本地文件

##### 编解码

原生

```shell
hex/unhex（自带）
数据put的时候，二进制数据乱码问题

md5
计算md5值（自带）
```

平台提供

```mysql
# 已经编译进hive源码，不需要再加载jar包
xl_urldecode() 

# 需要先加载jar包，字符串中有空格等的风险，如url参数传递，通常编码后再传
uridecode()/uriencode()函数
add jar $KK_WORKSPACE/bin/jar/com.xunlei.kk.feature.udf.jar
create temporary function uridecode as 'com.xunlei.kk.feature.udf.UDFURIDecoder';
create temporary function uriencode as 'com.xunlei.kk.feature.udf.UDFURIEncoder';
```

自定义

```mysql
# 使用python streaming处理,或者本地处理
```

##### 类型转换

**str->map**

> str_to_map(strings ,delim1,delim2), delin1键值对分隔符，delim2键值分隔符

```mysql
select str_to_map('k1:v1,k2:v2',',',':'); # {"k1":"v1","k2":"v2"}
```

**str->array**

> split(strings,pattern)

```mysql
select split('5.2.4.1234','\\.');  # ["5","2","4","1234"]
```

**array->str**

> concat_ws(delim,ARRAY arr)

```mysql
select concat_ws('_',fu5) from xmp_odl.xmpplaydur where ds='20170612' and hour=10 limit 10;
select concat_ws('_',["5","2","4","1234"]);
```

以上均是自带的，以下是扩展：

**array->map**

```python
# 比如k1,v1,k2,v2,其顺序依次是key,value,key,value,可以参考python-streaming实现
a = [1, 2, 3, 4, 5, 6]
b=list(zip( a[::2], a[1::2] )) # [(1, 2), (3, 4), (5, 6)]
dict(b) #{1: 2, 3: 4, 5: 6}
```

##### 分析函数

```mysql
#计算数组中某个值出现的次数
xl_array_count(array(b,b,a),string b); 
```

##### 反射Java

hive中提供了reflect函数来调用Java现有库中的方法，调用方法如下：

```mysql
select reflect("类名","方法名",参数1,参数2,...);
# 例如
select reflect("java.lang.Math","max",2.6,9.8); #9.8
select regexp_replace(reflect("java.util.UUID","randomUUID"),'-','');  
```



#### Streaming操作

hadoop streaming api为外部进程开始I/O管道，数据被传输给外部进程，外部进程从标准输入中读数据，然后将结果数据写入到标准输出。

注意：

> streaming过程使用到的文件都是本地文件，不需要上传到hadoop集群上

优点：

- 少数据量的复杂计算
- 快速出结果
- 几乎支持所有语言（bash/perl/python/java）

缺点：

- IO开销大，效率低

##### 语句

###### transform

结合insert overwrite 使用transform

```mysql
add file python_streaming.py;
select transform(substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time) 
using 'python_streaming.py' 
as (pid,mlint,flstr,sstr,fip,ftime)
from xmp_odl.xmpplaydur where ds='$date' limit 1000;
```

> 可以直接将经过处理后的文件进行处理后导出到本地

######  reduce

```mysql
add file t_stat_url_upload_split_mapper.py;
from(
    select iconv(furl,'gbk')  as furl,iconv(fip,'gbk') as fip,iconv(ftime,'gbk') as ftime
    from kankan_odl.t_stat_url_upload
    where ds='${date}'
    cluster by fip
)a
insert overwrite table kankan_bdl.t_stat_url_upload_split partition(ds='${date}')
reduce a.furl,a.fip,a.ftime
using 't_stat_url_upload_split_mapper.py'
as install,channel,peerid,version, package_name, installtype,fip,ftime ;
```

> 处理后插入到新表中

#####  实现

###### python

```shell
python实现
```

###### shell

shell脚本：`hive_streaming.sh`

```shell
#!/bin/bash
# substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time
# 2A5F8   [3,0,8] ["5486","0","0"]    0,1,0   124.91.9.111    1517673596
while read line;do
    infos=($line)
    echo -e -n "hahh:${infos[0]}\t${infos[1]}\t${infos[2]}\t${infos[3]}\t${infos[4]}\t"
    ds=`date -d @${infos[5]} "+%Y-%m-%d"`
    echo -e -n "${ds}\n"  
done

exit 0
```

hive语句：`hive_streaming.hql`

```mysql
-- 使用本地文件进行读取过滤，然后结果导出到本地
-- 2A5F8   [3,0,8] ["5486","0","0"]   0,1,0   124.91.9.111    1517673596
add file hive_streaming.sh; -- 加载streaming脚本
add file ban_ver; -- 加载本地文件
select transform(substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time)
using 'hive_streaming.sh'
as (pid,mlint,flstr,sstr,fip,ftime)
from xmp_odl.xmpplaydur where ds='20180204' limit 10;
```

###### perl

```perl
perl实现
```

### 积累

#### 细节

##### 注释

hql脚本注释

```mysql
# 单行注释
--i'm comment(回车)
select count(*) from dual;

# 多行注释
//暂时不支持
```

> 对比[mysql的注释](https://www.cnblogs.com/dapeng111/archive/2013/01/02/2842106.html)`xxx.sql`
>
> ```mysql
> # 这是mysql的单行注释
> select * from xx;
> ```

##### 中文别名

```mysql
select xx as `中文别名` from db.tbl;
# 注意其中文别名要用反双引号括起来，而不是单引号或者双引号

对于英文别名，直接写成 select xx as aliasxx,其中aliasxx不要再加引号
```

##### order by 字段

order by 是最后执行的，若对列(包含计算列)没有起别名，则\_c0,\_c1,\_c2分别对应相应的列

```mysql
use shoulei_bdl;
select 
    ds,
    guid,
    eventname,
    attribute1,
    from_unixtime(cast(ts as int),'yyyyMMdd HH:mm:ss') as t # 此处是否起别名对结果无影响
from 
   vvvvv
where 
    ds='20180327' and appid='48' and cv rlike '^5.32'
    and eventname!='ios_advertise' 
order by 
    ds,
    guid,
    t;  # 此处的t不能换成from_unixtime(cast(ts as int),'yyyyMMdd HH:mm:ss')，也不能换成ts
```

> 在orderby中可以使用别名

#### 字典数组
##### 数组集合

函数一览

| **Return Type** | **Name(Signature)**                    | **Description**                          |
| --------------- | -------------------------------------- | ---------------------------------------- |
| int             | size(Map<K.V>)                         | Returns the number of elements in the map type. |
| int             | size(Array<T>)                         | Returns the number of elements in the array type. |
| array<K>        | map_keys(Map<K.V>)                     | Returns an unordered array containing the keys of the input map. |
| array<V>        | map_values(Map<K.V>)                   | Returns an unordered array containing the values of the input map. |
| boolean         | array_contains(Array<T>, value)        | Returns TRUE if the array contains value. |
| array<t>        | sort_array(Array<T>)                   | Sorts the input array in ascending order according to the natural ordering of the array elements and returns it (as of version [0.9.0](https://issues.apache.org/jira/browse/HIVE-2279)). |
| array           | collect_set(col)                       | Returns a set of objects with duplicate elements eliminated. |
| array           | collect_list(col)                      | Returns a list of objects with duplicates. (As of Hive [0.13.0](https://issues.apache.org/jira/browse/HIVE-5294).) |
| int             | find_in_set(string str,string strlist) | 返回str在strlist第一次出现的位置，strlist是用逗号分割的字符串。如果没有找该str字符，则返回0 |

例子：

```mysql
select find_in_set('ab','ef,ab,de'); -- 2
select find_in_set('cd','ef,ab,de'); -- 0 

select find_in_set('cd',concat_ws(',',array('ef','ab','de'))); --0
```

###### 应用场景

数组元素拼接

```shell
# 将数组元素拼接成字符串（数组元素是字符串）
select concat_ws('_',array('b','b','a'));

# 若数组元素不是字符串(则报错)
select concat_ws(',',array(2,NULL,1));
```

> 数组中的每个元素转换成字符串

数组排序

```mysql
select sort_array(array(2,NULL,1)); 	# [null,1,2]
select sort_array(array(5,1,2,3,null)); # [null,1,2,3,5]
select sort_array(array("a","b","q","d","e")); #["a","b","d","e","q"]
```

数组最大值和最小值(不展开)

```mysql
# 数组最大值
select sort_array(array(2,NULL,1))[size(array(2,NULL,1))-1];
select sort_array(arr1)[size(arr1)-1];

# 数组最小值
select a2,if(sort_array(a2)[0] is NULL,sort_array(a2)[1],sort_array(a2)[0]) 
from xmp_data_mid.high_test;
```

数组均值、中位数、最大值、最小值

```mysql
# 方法1：
select
    id
    ,avg(ed)
    ,max(ed)
    ,min(ed)
from xmp_data_mid.high_test
lateral view explode(a1)ed as ed
group by id;

# 方法2
select id
    ,avg(ed)
    ,max(ed)
    ,min(ed)
from
(select id,ed
from xmp_data_mid.high_test
lateral view explode(a1)etd as ed
)t
group by id;
```

> 经过explode拆分的列可以直接参与select部分的计算，方法2主要用于验证

数组中元素出现的个数

```mysql
# 展开式
select
    id
    ,ed
    ,count(*)
from xmp_data_mid.high_test
lateral view explode(a1)ed as ed
group by id,ed;
```

##### 字典

###### map类型

函数一览：

| 函数名        | 用法             | 备注           |
| ---------- | -------------- | ------------ |
| map_keys   | map_keys(xx)   | 返回map所有key   |
| map_values | map_values(yy) | 返回map所有value |
|            |                |              |

额外函数：

| 函数名              | 用法                                                         | 备注                                               |
| ------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| xl_map_get(map,key) | select nvl(m2["k1"],''),nvl(xl_map_get(m2,"k1"),'') from high_test; | 获取map中指定的key值                               |
| xl_map_tag(v,map()) | select xl_map_tag('push_new',map('^1ps232','1','.\*push.\*','2')); --2 | 根据字段的值进行匹配，翻译成不同的值，类似维表翻译 |
| xl_str_tag(x,x)     | 还有问题待升级                                               |                                                    |

> ```mysql
> # 查看key中是否含有某项
> array_contains(map_keys(gameinfo),'wow')
> 
> # xl_map_tag使用（map的顺序对最后的结果影响很大）
> xl_map_tag(lower($1),map(
> 	 'dl_create.*','1',
> 	 'play.*(start|end)','1',
> 	 'search_start_1|search_1_submit|sniff_1_start|browser_web_pv','1',
> 	 'pay_success','1',
> 	 'push_click','1',
>      ));
> ```

**取值**

```mysql
select b['key1'] from xmp_data_mid.map_test;
select if(b['key1'] is null,'kong',b['key1']) from xmp_data_mid.map_test;
select nvl(b['key1'],'kong') from xmp_data_mid.map_test;

# 如果map里嵌了一个map，则里面的map的是字符串，不能直接被查询
```

**转化**

```mysql
# 将字符串转化为map类型
select str_to_map('1=2&3=4','&','='); 
# --结果：{"1":"2","3":"4"}
select str_to_map('1=2&3=4','&','=')['1']; 

```

**合并和分解**

从map类型中选出指定的key，组成一个新的map

```mysql
//待完成
```

**插入**

```mysql
# map类型可以直接插入到另一个map类型中
insert into xmp_data_mid.map_test select 'vvvv',b from xmp_data_mid.map_test;

# 组合普通字段成map格式插入到map类型中

```

###### json格式

**取值**

```mysql
# 从json字符串中取值

# 方法1：get_json_object
get_json_object(string json_string, string path)
# select a.timestamp, get_json_object(a.appevents, ‘$.eventid’), get_json_object(a.appenvets, ‘$.eventname’) from log a;

# 方法2：json_tuple
select a.id,b.* from xmp_data_mid.struct_test a 
lateral view json_tuple('{"name":"zhou","age":30}','name','age')b as f1,f2;
```

> 注意json字符串不能连续的取值，要用以下的方式：
>
> ```mysql
> get_json_object(get_json_object(content,'$.ed'),'$.clickid') as clickid
> ```

**转化**

```mysql
# json字符串转map对象（原生方法）
select regexp_replace('{"张":"二","李":"小"}','\\}|\\{', '');
select str_to_map(regexp_replace('{"张":"二","李":"小"}','\\}|\\{', ''));
-- 转化的结果是：{"\"李\"":"\"小\"","\"张\"":"\"二\""}

select regexp_replace('{张:二,李:小}','\\}|\\{', '');
select str_to_map(regexp_replace('{张:二,李:小}','\\}|\\{', ''));
-- 转化的结果是：{"李":"小","张":"二"}

# json字符串转map对象（自定义）
select xl2_json_map_habbo('{"userid":"228771123","is_year":"0","tq_id":"04","switch_type":2}')['userid']; 
-- 结果输出  228771123
```

> str_to_map():
>
> 将字符串str按照指定分隔符转换成Map，第一个参数是需要转换字符串，第二个参数是键值对之间的分隔符，默认为逗号`,`;第三个参数是键值之间的分隔符，默认为`=`（也有一说为`:`）

**合并和分解**

```json
{"redbao":'android','isnew':'new'}
{"redbao":'android','isnew':'new'}
{"redbao":'ios','isnew':'false'}
{"redbao":'ios','isnew':'new'}

# 合并结果
{
  "red":取redbao的结果，
  "new":取isnew的结果
}
```

==例子-展开：==

 ```shell
# 数据形式如下:
f1  f2  '[{"name":"张一","age":10,"sex":"girl"},{"name":"李一","age":12,"sex":"boy"}]'
f3  f4  '[{"name":"张二","age":10,"sex":"girl"}]'
f5  f6  '[{"name":"张三","age":10,"sex":"girl"},{"name":"李三","age":12,"sex":"boy"}]'


# 要解析成的格式
f1	f2 张一	10 girl
f1	f2 李一	12 boy
f3	f4 张二	10 girl
f5	f6 张三	10 girl
f5	f6 李三	12 boy
 ```

> 解决方案1：正则分割

```mysql
# split的分割符合支持正则，也就是支持完整的正则，包含断言
select split('{"name":"张一","age":10,"sex":"girl"},{"name":"李三","age":12,"sex":"boy"}','(?<=\\}),');
```

> 解决方案2：展开合并

```mysql

```

> 解决方案3：Streaming

```mysql

```

> 解决方案4：本地解析

```mysql

```

==例子-反转：==

```shell
# 待解析的格式
f1	f2	pos1	10
f1	f2	pos2	12
f3	f4 	pos1	13
f5	f6 	pos2	14
f5	f6 	pos3	18

# 要解析成的格式
f1 f2 {"pos1":10,"pos2":12}
f3 f4 {"pos1":13}
f5 f6 {"pos1":14,"pos2":18}
```

> 解决方案1：

```mysql

```

==例子-解析：==

```
id=xxxx,sessionid=xxx,rn=1,cur_episode=1,episodes=12,isover=0,year=2016,score=5.4;
id=xxxx,sessionid=xxx,rn=3,,cur_episode=12,episodes=12,isover=1,year=2017,score=9.2;
```

> 解决方案1：

```mysql
select
   guid
   ,pos_video -- 此处已经是分拆之后的形式了
   ,str_to_map(pos_video,',','=')['id'] as v_id -- 在分拆的形式上直接进行其它操作
   ,extdata_map['channel'] as v_type
from
    shoulei_bdl.bl_shoulei_event_fact
lateral view explode(split(extdata_map['contentlist'],'\073'))eds as pos_video
where ds='20180717' and appid='45' and type in ('video','other')
    and attribute1 in ('onlinePlay_channel_show')
```


#### 特殊处理

##### http请求头

###### 请求url

上报的url大多都经过uriencode进行编码，对`[:?,/]`等进行编码，若要正常解析，先使用uridecode对url解析，如下：

```mysql
# 解析前：
http%3A%2F%2Flist.v.xunlei.com%2Fv%2Ctype%2Cgenre%2F5%2Cteleplay%2Cjd%2Fpage6%2F
# 解析后
http://list.v.xunlei.com/v,type,genre/5,teleplay,jd/page6/
```

此外还对中文字符进行了hex，要先反hex，并去掉其中的`%`,如下：

```
# unhex前
http://48.fans.xunlei.com/catalog/catalog.shtml?type=%E9%9F%B3%E4%B9%90
# unhex后
http://48.fans.xunlei.com/catalog/catalog.shtml?type=音乐
```

综述，完整的hive还原url语句是：

```mysql
unhex(regexp_replace(parse_url(uridecode(fu4),'QUERY','type'),'%',''))
```

**参数解析**

```mysql
select parse_url('http://facebook.com/path/p1.php?query=1', 'PROTOCOL') from dual;  
# 返回结果：http
select parse_url('http://facebook.com/path/p1.php?query=1', 'HOST') from dual;
# 返回结果：facebook.com
select parse_url('http://facebook.com/path/p1.php?query=1', 'REF') from dual;
# 返回结果：空
select parse_url('http://facebook.com/path/p1.php?query=1', 'PATH') from dual;
# 返回结果：/path/p1.php
select parse_url('http://facebook.com/path/p1.php?query=1', 'QUERY') from dual;
# 返回结果:query=1
select parse_url('http://facebook.com/path/p1.php?name=zhang&age=12','QUERY','name') from dual;
# 返回结果:zhang
select parse_url('http://facebook.com/path/p1.php?query=1', 'FILE') from dual;
# 返回结果：/path/p1.php?query=1
select parse_url('http://facebook.com/path/p1.php?query=1', 'AUTHORITY') from dual;
# 返回结果：facebook.com
select parse_url('http://facebook.com/path/p1.php?query=1', 'USERINFO') from dual;
# 返回结果：空
```
例子：

```shell
# 纯路径
url_pure="concat(parse_url(xl_urldecode(xl_urldecode(url)),'HOST'),parse_url(xl_urldecode(xl_urldecode(url)),'PATH'))"

# 直接解析
select concat(parse_url('https://pay.xunlei.com/bjvip.html?referfrom=v_pc_xl9_push_noti_nfxf','HOST'),parse_url('https://pay.xunlei.com/bjvip.html?referfrom=v_pc_xl9_push_noti_nfxf', 'PATH'));
//结果：pay.xunlei.com/bjvip.html
```

###### 请求UA

[UA的格式](https://blog.csdn.net/laozhaokun/article/details/42024663)如下：

```shell
Mozilla/5.0 (Linux; Android 8.0; VKY-AL00 Build/HUAWEIVKY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/10.9 baiduboxapp/10.9.5.10 (Baidu; P1 8.0.0)
```

UA各部分的内容构成：

```

```

[UA解析](https://github.com/hotoo/detector)：

```mysql
npm install detector -g
#Usage: detector [options] "user-agent string.",解析示例如下：
detector 'Mozilla/5.0 (Linux; Android 5.0.2; vivo X5Pro D Build/LRX21M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/5.5.2.2'

   Device:  vivo@x5pro
       OS:  android@5.0.2
  Browser:  chrome@62.0.3202.84
   Engine:  webkit@537.36
```

##### ip处理

通过ip处理，获取位置（省份、市）等信息

ipstr->int

```mysql
#类似mysql:select inet_aton('59.54.109.78');
```

int->ipstr

> 暂时没有查找到关于ip的函数，需要自定义实现

```mysql
# 类似mysql:select inet_ntoa(993422670);
```

例子

```mysql
select xl_geoip_parse('59.54.109.78','ISP') #{"isp":"电信"}

# 准备工作：将整型ip（字符格式）转化成字符串
xl_inet_ntoa(xl_htonl(cast(serverinfo[1] as bigint)))

# 解析供应商（名称）
nvl(xl_geoip_parse(xl_inet_ntoa(xl_htonl(cast(serverinfo[1] as bigint))), 'ISP')['isp'],'unknow') as isp

# 解析省份（名称）
nvl(xl_geoip_parse(xl_inet_ntoa(xl_htonl(cast(serverinfo[1] as bigint))),'PROVINCE')['prov'],'unknow') as province

#　解析市（名称）
nvl(xl_geoip_parse(xl_inet_ntoa(xl_htonl(cast(serverinfo[1] as bigint))),'CITY')['city'],'unknow') as city
```

> ==xl_geoip_parse:==
>
> ```shell
> 第一个参数ip（字符串，例如：59.54.109.78）
>
> 第二个参数可选值：COUNTRY，COUNTRY_CODE，CITY，CITY_CODE，ISP，ISP_CODE，PROVINCE， PROVINCE_CODE，ALL，ALL_CODE 
> 返回值为map结构，当参数为ALL时，返回值如下
> {"prov":"广东省","isp":"电信","city":"深圳","country":"中国"}
>
> 例子（注意返回的是字典）：
> hive> select xl_geoip_parse(xl_inet_ntoa(xl_htonl(1315780155)),'city');
> {"city":"九江市"}
> ```
>
> xl_inet_ntoa
>
> ```shell
> 整型ip转字符串
> ```
>
> xl_htonl
>
> ```shell
> 大端ip数值转小端
> ```

##### 文件名处理

文件名及后缀解析

```mysql
# 方法1
filename_url="regexp_extract(${url_pure},'[^/]*$',0)"
filesuffix="substr(regexp_extract(${filename_url},'\\\.[a-zA-Z0-9]+$',0),2)"
filename_pure="case when length(${filesuffix})>0 then substr(xl_urlencode(${filename_url}),1,length(xl_urlencode(${filename_url}))-length(${filesuffix})-1) when length(${filesuffix})=0 then xl_urlencode(${filename_url}) end"

# 方法2
filename_2="regexp_extract(xl_urldecode(xl_urldecode(filename)),'[^/]*$',0)"
filename_ffix="substr(regexp_extract(${filename_2},'\\\.[a-zA-Z0-9]+$',0),2)"
filename_p="case when length(${filename_ffix})>0 then substr(xl_urlencode(${filename_2}),1,length(xl_urlencode(${filename_2}))-length(${filename_ffix})-1) when length(${filename_ffix})=0 then xl_urlencode(${filename_2}) end"

# 方法3：使用子查询的方式
local hql="$MUDF;insert overwrite table xmp_mid.gcid_purefilename_filter partition(ds='$date') 
                select distinct x.gcid,split(x.filename,'\\\\\\\\')[x.cnt-1] as fname from(
                select gcid,filename,size(split(uridecode(filename),'\\\\\\\')) as cnt from 					download_bdl.bl_downloadlib_download_fact   where ds='$date' and eventid in 					(4635,4637,4638) and service_name='pc.thunder9' and gcid!='')x;"
```

##### 关键词过滤

> 关键词过滤的核心是如何批量处理关键词的问题,目前唯一的解决方案是python streaming
>

#### 行列转换

##### 分列

| ID    | type_flag | tags                                     |
| ----- | --------- | ---------------------------------------- |
| 10001 | 3         | 11\_20_30,11\_22\_34,12\_23\_30,13\_24\_36 |
| 10002 | 2         | 11\_20,11\_22,12\_23,13\_24              |
| 10003 | 1         | 11,12                                    |

```mysql
# 参考列转行部分的例子
```

##### 列转行

包含列拆分

###### explode

将列数据展开成行数据

```mysql
select explode(array(1,2,3));

# 展开array成每行一个
select explode(b) from xmp_data_mid.array_test;

# 展开map成k，v的形式，每行一个kv对
select explode(b) as (k,v) from xmp_data_mid.map_test;
```

> 注意：explode不能和其它列混合使用，例如
>
> ```mysql
> select guid,explode(b) from xmp_data_mid.array_test;
> #会提示：
> -- UDTF's are not supported outside the SELECT clause, nor nested in expressions
> ```
>
> 解决办法参见下面的lateral view

###### lateral view

将拆分的数据作为新列数据，就像独立的列一样

```mysql
# array拆分成行
select fu1,fu2s from xmp_data_mid.xmpplaydur_test lateral view explode(fu2)b as fu2s limit 10;

# map拆分成行(每个kv对再和维度字段进行组合)
select a,k,v from xmp_data_mid.map_test lateral view explode(b)be as k,v limit 10;
select id,k,v from xmp_data_mid.high_test lateral view explode(m1)be as k,v limit 10;
```

在拆分的新列上进行统计操作

```mysql
select k,sum(v) from xmp_data_mid.high_test lateral view explode(m1)be as k,v group by k;
```

[**例子**](https://blog.csdn.net/dreamingfish2011/article/details/51250641)

列转行同时存在分列的情况

源表：

| ID    | type_flag | tags                                     |
| ----- | --------- | ---------------------------------------- |
| 10001 | 3         | 11\_20_30,11\_22\_34,12\_23\_30,13\_24\_36 |
| 10002 | 2         | 11\_20,11\_22,12\_23,13\_24              |
| 10003 | 1         | 11,12                                    |

需要转化成的结果表样子如下：

| ID    | type_flag | tag1 | tag2 | tag3 |
| ----- | --------- | ---- | ---- | ---- |
| 10001 | 3         | 11   | 20   | 30   |
| 10001 | 3         | 11   | 22   | 34   |
| 10001 | 3         | 12   | 23   | 30   |
| 10001 | 3         | 13   | 24   | 36   |
| 10002 | 2         | 11   | 20   |      |
| 10002 | 2         | 11   | 22   |      |
| 10002 | 2         | 12   | 23   |      |
| 10002 | 2         | 13   | 24   |      |
| 10003 | 1         | 11   |      |      |
| 10003 | 1         | 12   |      |      |

实现:

```mysql
-- step2:再分列
select
	id,
	type_flag,
    (case when type_flag in(1, 2, 3) then tag[0] else '' end) as tag1,
    (case when type_flag in(2, 3) then tag[1] else '' end) as tag2,
    (case when type_flag in(3) then tag[2] else '' end) as tag3
from
(-- step1:先列转行
select 
	id,
	type_flag,
	split(tags,'_') as atag 
from 
	high_test 
lateral view explode(tags)t1 as tag0
)a;
```

> 该方法需要先求出最大的type_flag,然后才能决定分多少列

##### 行转列

###### [group_concat](https://blog.csdn.net/gdp5211314/article/details/8794404)

```mysql
# 列出相等
SELECT group_concat(town) FROM `players` group by town;

# 列出所有
SELECT group_concat(town)　FROM players;
```

> 这个函数目前似乎没有实现，在mysql中也有，替代解决方案是下午的collect_set[list]
>
> ```mysql
> select s1,concat_ws('|',collect_set(s3)) from high_test group by s1;
> ```

###### collect_set[list]

```mysql
select s1,collect_set(s3) from high_test group by s1;
```

> 使用这种方式要注意数据和元素的对应关系，即键数组和值数组中的元素释放一一对应

###### group by sum(if)

```mysql
select s1,
	if(a1[0]>'d','>d','<d') as flag1,
	sum(if(n1>0,1,0)) as bg0,
	sum(if(n1>2,1,0)) as bg1 
from 
	xmp_data_mid.high_test 
group by s1,
	if(a1[0]>'d','>d','<d');
```

> 这个函数主要针对数字型

###### inner join

```mysql
select a.id,a.f1,b.f2,c.f3 
(select id,f1 from tbl where flag='xx')a
inner join 
(select id,f2 from tbl where flag='yy')b
on a.id=b.id
inner join 
(select id,f3 from tbl where flag='zz')c
on a.id=c.id;
```

> 这种方法主要针对字符串这种类型

**例子**

```mysql

```

#### 抽样

如何对数据进行抽样,

##### GTopN抽样

```mysql
# 每组前N个
use xmp_data_mid;
SELECT A.ds, A.srctbl, A.srcdb,A.datasize
  FROM (SELECT T.ds,
               T.srctbl,
               T.srcdb,
               T.hour,
               T.datasize,
               RANK() OVER(PARTITION BY T.srctbl ORDER BY T.datasize DESC) RK
          FROM group_test T) A
 WHERE RK < 4;
```

##### 间隔抽样

```mysql
# 排序后间隔抽样挑选
select 
	* 
from
(
    select 
        play_duration,
        play_starttime,
        play_endtime,
        rank() over (order by play_duration) as rn
    from 
        shoulei_bdl.bl_shoulei_play_native 
    where ds='20180525' and appid='45'
)a
where rn%1000=0;
```

##### [随机抽样](https://blog.csdn.net/zwj841558/article/details/71143493)

要求根据员工的职级分类rank，然后每类职级随机抽取2条数据， 

```mysql
select 
   id,
   name,
   age,
   rank
from 
( 
    select id,
        name,
        age,
        rank,
        row_number()over(partition by rank order by rand()) as rn
    from tab_a 
) t
where t.rn <=2
```

#### 分布

分布其实也是指定时间内的频次统计，分为宽格式和长格式两种方式

##### 宽格式

```mysql
select
    cdays
    ,count(*)
    ,collect_set(guid)
from
(
    select 
        guid
        ,count(distinct ds) as cdays
    from
        shoulei_bdl.bl_shoulei_event_fact
    where ds>='20180601' and ds<='20180612' and appid='45'
        and type='other'
        and attribute1='per_integral_task_click'
        and extdata_map['stat']='get'
    group by guid
)a
group by cdays;
```

> 备注:原始low版
>
> ```mysql
> select
>     cdays
>     ,count(*)
>     ,collect_set(guid)
> from
> (
>     select 
>         guid
>         ,count(*) as cdays
>     from
>     (
>         select 
>             distinct ds,
>             guid
>         from
>             shoulei_bdl.bl_shoulei_event_fact
>         where ds>='20180601' and ds<='20180612' and appid='45'
>             and type='other'
>             and attribute1='per_integral_task_click'
>             and extdata_map['stat']='get'
>     )a
>     group by guid
> )b
> group by cdays;
> ```

##### 长格式

```mysql
select
    cdays
    ,users
    ,uid
from
(
    select
        cdays
        ,count(*) as users
        ,collect_set(userid) as uids 
    from
    (
        select 
            userid
            ,count(distinct ds) as cdays
        from
            shoulei_bdl.bl_shoulei_event_fact
        where ds>='20180601' and ds<='20180603' and appid='45'
            and type='other'
            and attribute1='per_integral_task_click'
            and extdata_map['stat']='get'
        group by userid
    )a
    group by cdays
)b
lateral view explode(uids)ud as uid;
```

#### 探索

##### 错位间隔

错位间隔问题主要处理行之间的差值，主要在已排序的情况下，用以计算指定条件下的间隔计算问题,该技能可用于分析用户log。（扩展到mysql实现）

| id   | s1   | rn1(排序生成) |
| ---- | ---- | ------------- |
| b1   | 1    | 1             |
| a1   | 4    | 2             |
| a1   | 6    | 3             |
| a1   | 8    | 4             |
| c1   | 12   | 5             |
| b1   | 20   | 6             |
| a1   | 32   | 7             |
| c1   | 45   | 8             |
| a1   | 67   | 9             |
| a1   | 99   | 10            |

> ```mysql
> select * from xmp_data_mid.tbl_a where dtask='dur';
> # 后面为了方便，扩展了rn1字段到另外的一张表：xmp_data_mid.tbl_a_view
> ```

1、两个a1之间插入的记录数

>  解题思路：排序后选出所有的a1值，下面的减上面的

```mysql
select
    id
    ,rn1
    ,rn1-rn2 as pos_diff
from
(
    select
        id
        ,rn1
        ,lag(rn1,1,0) over(order by rn1) as rn2
    from
    (
        select
            id
            ,rn1
        from
        (
            select id
                ,s1
                ,row_number() over(order by cast(s1 as int)) as rn1
            from
                xmp_data_mid.tbl_a
            where dtask='dur'
        )a
        where id='a1'
    )b
)c
where rn2!=0;
```

> 数据结果：
>
> ```
> a1      3       1
> a1      4       1
> a1      7       3
> a1      9       2
> a1      10      1
> ```

2、两个a1之间的s1之差

```mysql
select
    id
    ,rn1
    ,rn1-rn2 as pos_diff
    ,s1
    ,s2
    ,s1-s2 as value_diff
from
(
    select
        id
        ,rn1
        ,lag(rn1,1,0) over(order by rn1) as rn2
        ,s1
        ,lag(s1,1,0) over(order by rn1) as s2
    from
    (
        select
            id
            ,s1
            ,rn1 
        from
        (
            select id
                ,s1
                ,row_number() over(order by cast(s1 as int)) as rn1
            from 
                xmp_data_mid.tbl_a
            where dtask='dur'
        )a
        where id='a1'
    )b
)c
where rn2!=0;
```

> 查询结果：
>
> ```
> a1      3       1       6       4       2.0
> a1      4       1       8       6       2.0
> a1      7       3       32      8       24.0
> a1      9       2       67      32      35.0
> a1      10      1       99      67      32.0
> ```

3、两个a1之间没有c1插入情况下的插入记录数

```mysql
select
    c.id
   ,c.s1
   ,c.s1_pre
   ,c.s1-c.s1_pre
   ,c.rn1
   ,c.rn1_pre
   ,c.rn1-c.rn1_pre as pos_diff
from
(
    -- 原值选择
    select 
        id
        ,s1
        ,lag(s1,1,0) over(order by rn1) as s1_pre
        ,rn1
        ,lag(rn1,1,0) over(order by rn1) as rn1_pre
    from 
        xmp_data_mid.tbl_a_view
    where id='a1'
)c
left join
(
    select
        distinct a.rn1 as rn1
    from
    (
        -- 原值条件准备
        select 
            rn1
            ,lag(rn1,1,0) over(order by rn1) as rn1_pre
        from 
            xmp_data_mid.tbl_a_view
        where id='a1'
    )a
    full join
    (
        -- 过滤
        select 
            rn1
        from 
            xmp_data_mid.tbl_a_view
        where id='c1'
    )b
    where a.rn1_pre<b.rn1 and b.rn1<a.rn1
        and a.rn1_pre!=0  
)d
on c.rn1=d.rn1
where d.rn1 is null and c.rn1_pre!=0;
```

> 查询结果：
>
> ```
> a1      6       4       2.0     3       2       1
> a1      8       6       2.0     4       3       1
> a1      99      67      32.0    10      9       1
> ```

4、两个a1之间没有c1插入情况下的s1之差

```mysql
参见3，完全实现
```



### 优化

优化方向:

- 好的模型设计事半功倍
- 解决数据倾斜问题，set hive.groupby.skewindata=true;
- 减少job数
- 设置合理的map reduce的task数，能有效提升性能
- 对count(distinct)采取漠视的方法，尤其数据大的时候很容易产生倾斜问题
- 小文件合并
- 把握整体，单个作业的最优不如整体的最优

#### 设置参数

参数一览

| 设置                                       | 意义     | 备注   |
| ---------------------------------------- | ------ | ---- |
| hive.auto.convert.join=true;             |        |      |
| hive.auto.convert.join.noconditionaltask = true; |        |      |
| hive.auto.convert.join.noconditionaltask.size = 250000000; |        |      |
| set hive.exec.mode.local.auto=true;      | 开启本地模式 |      |
|                                          |        |      |

```shell
In order to change the average load for a reducer (in bytes):
  set hive.exec.reducers.bytes.per.reducer=<number>
In order to limit the maximum number of reducers:
  set hive.exec.reducers.max=<number>
In order to set a constant number of reducers:
  set mapreduce.job.reduces=<number>
```

设置样例

```shell
HIVE="/usr/local/complat/cdh5.10.0/hive/bin/hive  
-hiveconf mapreduce.job.name=xxstat_hive 
-hiveconf mapred.job.queue.name=root.shoulei

# 输入输出
-hiveconf hive.exec.compress.output=true 
-hiveconf hive.exec.compress.intermediate=true
-hiveconf io.seqfile.compression.type=BLOCK 
-hiveconf hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat 
-hiveconf mapreduce.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec 

-hiveconf hive.map.aggr=true
-hiveconf hive.stats.autogather=false  

# 动态分区
-hiveconf hive.exec.dynamic.partition=true
-hiveconf hive.exec.dynamic.partition.mode=nonstrict

# 小文件合并
-hiveconf mapreduce.max.split.size=100000000 
-hiveconf mapreduce.min.split.size.per.node=100000000 
-hiveconf mapreduce.min.split.size.per.rack=100000000

# join配置
-hiveconf hive.auto.convert.join=false

# 数据倾斜处理
-hiveconf hive.groupby.skewindata=false"
```

##### 设置reduce的个数

```shell
set mapred.reduce.tasks=18;

# 设置最大reduce的个数
set hive.exec.reducers.max=128;
```

##### 开启本地模式

```mysql
hive> set hive.exec.mode.local.auto=true;(默认为false)

#当一个job满足如下条件才能真正使用本地模式：
1.job的输入数据大小必须小于参数：hive.exec.mode.local.auto.inputbytes.max(默认128MB)
2.job的map数必须小于参数：hive.exec.mode.local.auto.tasks.max(默认4)
3.job的reduce数必须为0或者1
```


#### 数据倾斜

```shell
set hive.groupby.skewindata=true;
```

注意下面语句的报错：

```mysql
-- hive优化公共项
-- 合并小文件
set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat;
set mapreduce.max.split.size=100000000;
set mapreduce.min.split.size.per.node=100000000;
set mapreduce.min.split.size.per.rack=100000000;

-- 设置reducer个数
set hive.exec.reducers.max=128;

-- 数据倾斜
set hive.groupby.skewindata=true;

-- 分组点击输入、点击评论区、点赞
select
    ds
    ,substr(guid,-1)
    ,'分组点击输入_点击评论区_点赞'
    ,sum(if(extdata_map['button']='input',1,0)) as click_input_cnt
    ,count(distinct if(extdata_map['button']='input',guid,NULL)) as click_input_user
    ,sum(if(extdata_map['button']='comment',1,0)) as click_comment_cnt
    ,count(distinct if(extdata_map['button']='comment',guid,NULL)) as click_comment_user
    ,sum(if(extdata_map['button']='comment_like',1,0)) as click_like_cnt
    ,count(distinct if(extdata_map['button']='comment_like',guid,NULL)) as click_like_user
from
    shoulei_bdl.bl_shoulei_event_fact
where
    ds>='20180511' and ds<='20180514'  and appid='45'
    and eventname='android_dl_center_action'
    and attribute1='dl_center_detail_click'
    and cv rlike '^5.58'
group by
    ds
    ,substr(guid,-1);
```

> FAILED: SemanticException [Error 10022]: DISTINCT on different columns not supported with skew in data

#### 合并小文件

```shell
# 合并小文件
set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat;
set mapreduce.max.split.size=100000000;
set mapreduce.min.split.size.per.node=100000000;
set mapreduce.min.split.size.per.rack=100000000;

# 设置reducer个数
set hive.exec.reducers.max=128;
```

> 备注:一般将数据倾斜和合并小文件放在一起使用

### 备份

#### 迁移

数据迁移指的是在不同的hive数据仓库或者不同的hive集群上进行数据的迁移

##### 结构迁移

结构迁移可以跨库

```mysql
create table db1.xxx like db2.xxx;
```

##### 结构和数据迁移

数据迁移的时候也可以直接跨库

```mysql
create table db1.xxx as select * from db2.xxx;
```

> 不确定分区是否也一起迁移了，或者迁移的数据是否也按分区

#### 导入

##### 文件导入

```mysql
# 基本
load data local inpath '/liguodong/hive/data' [overwrite]  into table test partition (country='china');

# 升级
ihql="use kankan_odl;delete from tbname where ds='${date}';
	  load data local inpath  '/home/work/test.txt' into table tbname;"
${HIVE} -e "{chql}"
```

> 注意`overwrite`的使用

##### 其它表

```mysql
insert [overwrite] into table tmp2 partition(ds='20180521') 
select attribute1,is_core,user_type,comment,appid 
from 
	ftbl_dim_shoulei_dau_flag 
where ds='20180521';
```

> 从其表的数据导入，注意分区的使用

#### 导出

##### 导出到文件

- 命令行输出重定向

```shell
hql="use kankan_odl;select '${date}',fu3,fu2,count(*) from xmpcloud2 where ds='{date}' and length(fu4)=16 group by fu3,fu2;"
${HIVE} -e "${hql}" > xmp_cloud_20161201
```

- 导出数据到本地文件(并[指定字段分割方式](https://www.2cto.com/database/201506/412250.html))

```sql
insert overwrite local directory '/data/access_log/access_log.45491' row format delimited fields terminated by '\t' collection items terminated by ',' select * from xx
```

##### 导出到其源

```mysql

```

### 问题

#### 面试

//待添加

#### 查询

##### join时候字段非相等操作

问题描述：

​	Both left and right aliases encountered in JOIN 's1'

解决方法：

```mysql
# 两个表join的时候，不支持两个表的字段 非相等 操作, 例如t2.dtlogtime>=t1.s1 
select t2.iuin 
from test.xxx t1 
join test.vvv t2 
	on ( t1.i0 = t2.iuin 
        and t2.par_datetime in ('201405') 
        and t2.dtlogtime>=t1.s1 and t2.Ireason not in (1003)
       );

# 可以将非相等条件提取到where中
select t2.iuin 
from test.xxx t1 
join test.vvv t2 
on ( t1.i0 = t2.iuin ) 
where  t2.par_datetime in ('201405') 
   and t2.dtlogtime>=t1.s1 
   and t2.Ireason not in (1003);
```

##### count distinct 和sum

![count distinct sum问题](http://tuling56.site/imgbed/2018-04-27_140239.png)

##### [hive cube rollup分组问题](https://blog.csdn.net/u011317245/article/details/52503170)

提示错误：

> FAILED: SemanticException [Error 10210]: Grouping sets aggregations (with rollups or cubes) are not allowed if aggregation function parameters overlap with the aggregation functions columns

例子如下：

```mysql
select 
    ds
    ,'首页影评卡片曝光和点击'
    ,attribute1
    ,nvl(extdata_map['cinecism_id'],'total') as cid
    ,substr(substr(guid,-2),1,1) as last_2
    ,substr(guid,-1) as last_1
    ,count(*) as cnt
    ,count(distinct guid) -- 人数
from
    shoulei_bdl.bl_shoulei_event_fact
where ds='20180417' and appid='45' and type='video'
    and cv rlike '^5.57'
    and eventname='android_hometab'
    and attribute1 in ('home_cinecism_show','home_cinecism_click')
    and extdata_map['cinecism_id'] is not null 
group by 
    ds
    ,attribute1
    ,extdata_map['cinecism_id']
    ,substr(substr(guid,-2),1,1)
    ,substr(guid,-1)
grouping sets((ds)
    ,(ds,attribute1,substr(substr(guid,-2),1,1),substr(guid,-1))
    ,(ds,attribute1,extdata_map['cinecism_id'],substr(substr(guid,-2),1,1),substr(guid,-1))
);

# 存在5个聚合条件，但是去掉count(distinct guid)这个计算人数的选项后，就可以使用了
```

##### [order by,sort by, distribute by, cluster by区别](https://blog.csdn.net/jthink_/article/details/38903775)

###### order by 

全局排序，最后所有的数据都会到同一个reducer进行处理，需要注意的是：

hive.mapred.mode=strict（默认值是nonstrict）,这时就必须指定limit来限制输出条数

###### sort by

每个reducer端都会进行排序，也就是保证局部有序，但是不能不保证全局有序（除非只有一个reducer),好处事进行了局部排序之后在进行全局排序就能提高不少的效率

######  distribute by和sort by

 ditribute by是控制map的输出在reducer是如何划分的,可以得到伪近似的全局排序

###### cluster by

```mysql
select mid, money, name from store cluster by mid  
# 等价于
select mid, money, name from store distribute by mid sort by mid  
```

​    如果需要获得与3中语句一样的效果：

```mysql
select mid, money, name from store cluster by mid sort by money  
```

​    注意被cluster by指定的列只能是降序，不能指定asc和desc。

##### reduce 卡在99%的数据倾斜问题

参见优化-数据倾斜，目前的处理方法是：

```shell
set hive.groupby.skewindata=true;
```

## 参考

- 基础

  [ApacheHive权威参考手册（推荐）](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.3.4/bk_dataintegration/content/new-feature-insert-values-update-delete.html)

  [官方参考手册（注意官方函数参考）](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DML#LanguageManualDML-Delete)

  [lxw的大数据田地(强烈推荐)](http://lxw1234.com/archives/2015/06/315.htm)

  [hive array、map、struct使用](http://blog.csdn.net/yfkiss/article/details/7842014)

  [hive map类型处理](http://blog.csdn.net/longshenlmj/article/details/41519453)

  [内部表和外部表的区别](http://blog.csdn.net/Dax1n/article/details/66979069)

  [表信息查看](http://blog.csdn.net/babyfish13/article/details/52055927)

  [hive数据类型转换](https://www.iteblog.com/archives/892.html)

  [Hive数据类型和函数参考大全（推荐）](https://blog.csdn.net/xiaolang85/article/details/8645647)

- 函数

  [HIVE2.0函数大全(推荐)](https://www.cnblogs.com/MOBIN/p/5618747.html#1)

  [HIVE函数大全和例子](https://blog.csdn.net/xianming2012/article/details/17372195)

  [HIVE 时间函数](http://www.cnblogs.com/moodlxs/p/3370521.html)

  [HIVE字符串函数](https://www.iteblog.com/archives/1639.html)

  [HIVE数学函数](http://blog.csdn.net/zhoufen12345/article/details/53608271)

  [HIVE常见内置函数及其使用(推荐)](http://blog.csdn.net/scgaliguodong123_/article/details/46954009)(还有要探索的地方)

  [HIVE窗口分析函数grouping sets、cube、roll up](http://lxw1234.com/archives/2015/04/193.htm)

  [HIVE窗口分析函数ntile、row_number、rank、dense_rank](http://lxw1234.com/archives/2015/04/181.htm)

- 查询

  [连接参考](http://www.cnblogs.com/pcjim/articles/799302.html)

  [hive join操作列表](http://lxw1234.com/archives/2015/06/315.htm)

- 积累

  [HIVE数据迁移](http://blog.csdn.net/u9999/article/details/34119441)

  [Hive SQL: Both left and right aliases encountered in JOIN](https://stackoverflow.com/questions/36015035/hiv	e-sql-both-left-and-right-aliases-encountered-in-join)

  [lateral view explode用法](http://blog.csdn.net/bitcarmanlee/article/details/51926530)

  [hive 高级数据类型使用之array（含横表转纵表)](https://blog.csdn.net/dreamingfish2011/article/details/51250641)

  [hive分组随机抽取](https://blog.csdn.net/zwj841558/article/details/71143493)

- 优化

  [hive优化-使用经验](http://www.aboutyun.com/thread-6047-1-1.html)

  [hive开启本地模式](http://blog.csdn.net/shenxiaoming77/article/details/43197441)

  [Hive join数据倾斜解决方案](http://www.cnblogs.com/ggjucheng/archive/2013/01/03/2842821.html)

  [hive map join使用和个人理解](https://blog.csdn.net/liuj2511981/article/details/8616730)

- 备份

  [load data指令小结（推荐）](https://www.cnblogs.com/tugeler/p/5133019.html)

- 问题​