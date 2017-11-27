## HIVE积累

[TOC]

### 基础

#### 数据类型

基本数据类型：tinyint, smallint, int,bigint, boolean, float, double, string

复杂数据类型：struct，map，array

##### 基本数据类型

**string**

```mysql
# 字符串分割(返回数组)
split('xxx_we2_23','_');  
```

##### 复杂数据类型

**array**

```mysql
# 求array的长度
size(arrya)
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

load data local inpath "array.txt"  overwrite into table array_test;
```

**map**

```mysql
select map("key1","val1") from test.dual; 

# 测试1：
insert into table xmp_data_mid.map_test values( 'hahh',map("key1","val1"));
# 则会报错：
# Unable to create temp file for insert values Expression of type TOK_FUNCTION not supported in insert/values
# 更改成：
insert into table xmp_data_mid.map_test select 'hahh',map("key1","val1") # from test.dual;



# 测试2：
insert into table xmp_data_mid.map_test select 'hahh','{"key2":"val2"}';
# 则会报错：
# FAILED: SemanticException [Error 10044]: Line 1:18 Cannot insert into target table because column number/types are different 'map_test': Cannot convert column 1 from string to map<string,string>.
# 更改成：
insert into table xmp_data_mid.map_test select 'hahh',str_to_map('{"key2":"val2"}');
# 插入结果
hahh    {"{\"key2\"":"\"val2\"}"}

insert into table xmp_data_mid.map_test select 'hahh',str_to_map('key3:val3,key4:val4');
```

例子：

```mysql
create table map_test(a string , b map<string, string>)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE;
load data local inpath "map.txt"  overwrite into table map_test;
```

> 注意:
>
> map的字典不能在order by中使用，需要使用别名
>
> ```mysql
> select mdict['xxx'] as mdx,mdict['vvv'] from db1.table1 order by  mdx;
> ```

**struct**

```mysql

```

例子：

```

```

**整体测试表：**

```mysql
create table group_test(ds string,srctbl string,srcdb string, hour string,datasize int)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE;
load data local inpath "group.txt"  overwrite into table group_test;
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

#### 创建表

创建库的时候最好指定下库的路径，建立内部表的时候不建议指定表的location的位置，如下格式：

```mysql
create database if not exists apple1_bdl comment 'apple1 without xiaomi bdl data'
location '/user/complat/warehouse/apple1_bdl.db/';
```

> 这是创建库而不指定库的路径的时候库的目录是/user/xxx/warehouse/,此处删除库的时候会直接将整个目录删除。

##### 文本格式存储
```sql
use kankan_odl;drop table if exists hive_table_templete;
create external table if not exists hive_table_templete(
  subid int,
  peerid string,
  movieid int)
partitioned by (ds string)
row format delimited
fields terminated by '\t'
stored as textfile;
```

> 只有文本存储格式才能使用load data local inpath的方法进行数据加载填充

##### 序列化格式存储

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
fields terminated by '\u0001'
stored as inputformat
  'org.apache.hadoop.mapred.SequenceFileInputFormat'
outputformat
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat'
```
#### 属性修改

##### 分区操作

###### 显示分区

`use xmp_odl;show partitions $tbl partition(ds='$date');`

###### 添加分区

`use xmp_odl;alter table $tbl add if not exists partition (ds='$date',hour='$hour');`

###### 删除分区

```mysql
use xmp_odl;
alter table $tbl drop if exists partition(ds='20160808',hour='00');

#例子
alter table odl_shoulei_adv_gdtinfo drop if exists partition (ds='$date');
```

> 问题：为什么在insert overwrite table之前一般都先使用这个语句删除对应的分区

###### 修改分区

```sql
use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') set location "/user/kankan/warehouse/..."

use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') rename to partition(ds='20160808',hour='01')
```

##### 列操作

###### 添加列

```mysql
use xmp_odl;
alter table $tbl add columns(col_name string);
```

###### 修改列

```mysql
use xmp_odl;
alter table $tbl change col_name newcol_name string [after x][first];
```

###### 删除列

`use xmp_odl;alter table $tbl drop?`

##### 表操作

参数设置,修改，存储格式，分桶

###### 表重命名

`use xmp_odl;alter table $tbl rename to new_tbl_name;`

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

> 对外部表（存储在本地文件系统）和内部表（存储在MetaStore），删除语句相同
>
> ` drop table if exists $tbl`

删除的时候会连分区和文件(内部表)一起删除

#### 数据导入导出

##### 导入数据

```shell
ihql="use kankan_odl;delete from tbname where ds='${date}';load data local inpath  '/home/work/test.txt' into table tbname;"
${HIVE} -e "{chql}"
```

##### 导出数据

- 命令行输出重定向

```shell
hql="use kankan_odl;select '${date}',fu3,fu2,count(*) from xmpcloud2 where ds='{date}' and length(fu4)=16 group by fu3,fu2;"
${HIVE} -e "${hql}" > xmp_cloud_20161201
```

- 导出数据到本地文件(并指定字段分割方式)

```sql
insert overwrite local directory '/data/access_log/access_log.45491' row format delimited fields terminated by '\t' collection items terminated by ',' select * from xx
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
select case when (fu6>=0 and fu6<1024) then '[0,1)' when (fu6>=1024 and fu6<2048) then '[1,3)' when (fu6>=2048 and fu5<3072) then '[2,3)' when (fu6>=3072 and fu6<4096) then '[3,4)' when fu6>=4096 then '[4,)' else 'error' end as 'dur',if((lower(fu7) regexp "geforce") ,'yes','no'),count(*) from xmp_odl.xmpcloud2 where ds='20170618' and fu3='2341' and fu2 in (3,4,5) group by substr(fu6,1,1),if(( lower(fu7) regexp "geforce"),'yes','no') order by tsize;
```

##### coalesce

COALESCE( value1,value2,... )

The COALESCE function returns the fist not NULL value from the list of values. If all the values in the list are NULL, then it returns NULL.

```mysql
select COALESCE(NULL,1,"ww") from test.dual;
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

hive中的正则转义使用两个反斜杠， 即‘//’，

 基础元字符：

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



```mysql
# 正则匹配
select  'abc'  regexp '^[a-z]*$'   from test.dual;
select  'http://v.xunlei.com'  regexp 'http://v.xunlei.com/?$'   from test.dual; //true

# 正则抽取（注意此处不能使用\d和\w等类似的字符）
select regexp_extract('http://xxx/details/0/40.shtml','http://xxx/details/([0-9]{1,})/([0-9]{1,})\.shtml',1) from test.dual; # 返回40

select regexp_extract('5.2.14.5672',"(^\\d+)\\.(\\d+)\\.(\\d+)",0); 
select regexp_extract('0796-7894145','(^\\d{3,4})\\-?(\\d{7,8}$)',1); //结果0796
select regexp_extract('https://pay.xunlei.com/bjvip.html?referfrom=v_pc_xl9_push_noti_nfxf','(.*)\\?referfrom=(.*)',1); //结果https://pay.xunlei.com/bjvip.html


# 正则替换
select regexp_replace('foobar','oo|ba','') from test.dual; # 返回fr

# 正则替换特殊字符--命令行版本
select regexp_replace('<李>{二}狗(张)|).%-+&【德! 】*[ 江 ]?','_|\\\|>|<|\\{|\\}|%|\\||!|@|#|$|\\s|\\[|\\]|\\.|\\?|\\*|【|】|，|\\(|\\)|：|&|-|\\+|:|。|','');

# 正则替换特殊字符--shell版
select regexp_replace('<李>{二}狗(张)|).%-+&【德! 】*[ 江 ]?','_|\\\\\\|>|<|\\\\{|\\\\}|%|\\\\||!|@|#|$|\\\\s|\\\\[|\\\\]|\\\\.|\\\\?|\\\\*|【|】|，|\\\\(|\\\\)|：|&|-|\\\\+|:|。|','');

# 正则分割
select split(fu1,'\\.') from xmp_odl.xmpcloud2 where ds='20170502' and hour=11 limit 10;
```

一个使用正则的聚合例子：

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

连接是在查询中最广泛使用的，但要注意数据倾斜问题

##### left outer join

left join(左连接)：返回两个表中连结字段相等的行和左表中的行；

>  左表(A)的记录将会全部表示出来,而右表(B)只会显示符合搜索条件的记录(例子中为: A.aID = B.bID).B表记录不足的地方均为NULL.

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

##### right outer join

right join(右联接)：返回包括右表中的所有记录和左表中联结字段相等的记录。

> right outer join的结果刚好相反,这次是以右表(B)为基础的,A表不足的地方用NULL填充.

```

```

##### full outer join

全外连接

```

```

##### inner join

inner join(等值连接)：只返回两个表中连接字段相等的行；

```mysql
SELECT
	persons.lastname,
	persons.firstname,
	orders.orderno
FROM
	persons
INNER JOIN orders ON persons.id_p = orders.id_p
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

连接小表的时候，在内存中操作，省去reduce过程,和common join存在着差别

```mysql
设置参数：
set hive.auto.convert.join=true;
set hive.mapjoin.smalltable.filesize=250000
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

一般函数

```mysql
（1）length(stringA)：返回字符串长度

（2）concat(stringA, string B...)：
     合并字符串，例如concat('foo','bar')='foobar'。注意这一函数可以接受任意个数的参数

（3）substr(stringA, int start) substring(string A,int start)：
     返回子串，例如substr('foobar',4)='bar'

（4）substring(string A, int start,int len)：
     返回限定长度的子串，例如substr('foobar',4, 1)='b'

（5）split(stringstr, string pat)：
     返回使用pat作为正则表达式分割str字符串的列表。例如，split('foobar','o')[2] = 'bar'。

（6）getkeyvalue(str,param) # 自定义
     从字符串中获得指定 key 的 value 值 UDFKeyValue
     CREATE TEMPORARY FUNCTION getkeyvalue  AS 'com.taobao.hive.udf.UDFKeyValue';
```

字符串分割

```mysql
# 一般字符
select split('a,b,c,d',',')[0] from test.dual;
# 特殊字符
split('192.168.0.1','\\.') from test.dual;
# 在shell脚本或者“”内
当然当split包含在 "" 之中时 需要加4个\，如 
hive -e "....  split('192.168.0.1','\\\\.') ... "  不然得到的值是null
```

> 注意：当待分割的字符串是空或者null的时候，使用size(split('cw3ew3','xx'))得到的数组长度却是1，可通过以下方式修正：
>
> select if(length('')==0,0,size(split('','_'))) from test.dual;

字符串截取

```mysql
select substr('123456',0,2) from test.dual; # 其等价于substr('123456',1,2),从0开始和从1开始的结果是相同的
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

##### 日期时间

基本操作

```mysql
# 整型时间戳转日期
select from_unixtime(finsert_time,'yyyyMMdd HH:mm:ss') from xmp_odl.xmp_pv where ds='20161206';

# 日期转时间戳
select unix_timestamp('20111207 13:01:03','yyyyMMdd HH:mm:ss') from test.dual;

# 获取日期小时和分
select substr('2011-12-07 13:01:03',1,16) from test.dual;  #2011-12-07 13:01

# 统计小时内的最高值
select hour(ftime),count(distinct fpeerid) cnt from xmp_odl.t_stat_play where ds='20170708' group by hour(ftime) order by cnt desc;

# 统计五分钟的最高值
select collect_set(substr(ftime,1,16))[0],int((hour(ftime)*60+minute(ftime))/5),count(distinct fpeerid) cnt from xmp_odl.t_stat_play where ds='20170908' group by int((hour(ftime)*60+minute(ftime))/5) order by cnt desc;

# 统计每10秒内的最高值
select collect_set(ftime)[0],int((hour(ftime)*3600+minute(ftime)*60+second(ftime))/10),count(distinct fpeerid) cnt from xmp_odl.t_stat_play where ds='20170908' group by int((hour(ftime)*3600+minute(ftime)*60+second(ftime))/10) order by cnt desc;
```

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

（4）date_format(date,date_pattern)
     CREATETEMPORARY FUNCTION date_format AS'com.taobao.hive.udf.UDFDateFormat';
     根据格式串format 格式化日期和时间值date，返回结果串。
     date_format('2010-10-10','yyyy-MM-dd','yyyyMMdd')
     date_format('2010-12-23','yyyyMMdd');

（5）str_to_date(str,format)  # 自定义
     将字符串转化为日期函数
	 CREATE TEMPORARY FUNCTION str_to_date AS 'com.taobao.hive.udf.UDFStrToDate';
     str_to_date('09/01/2009','MM/dd/yyyy')
```

参考:[HIVE时间操作函数](http://www.cnblogs.com/moodlxs/p/3370521.html)

##### 数学函数

- 窗口函数
  - 分区排序
  - 动态GroupBy
  - TopN
  - 累计计算
  - 层次查询
- 分析函数
  - RANK
  - ROW_NUMBER
  - DENSE_RANK
  - CUME_DIST
  - PERCENT_RANK
  - NTILE
- 混合函数
  - ava_method(class,method [,arg1 [,arg2])
  - reflect(class,method [,arg1 [,arg2..]])
  - hash(a1 [,a2...])

###### 窗口函数

- lead
- lag
- first_value
- last_value

###### 分析函数

- cume_dist

- row_number

- percent_rank

- ntile

  按层次查询

- percentile

  返回分位点对应的记录值

- 累计函数

  计算一定范围内、一定值域内或者一段时间内的累积和以及移动平均值等

- rank()/dense_rank()

```mysql
# 统计每组前N个
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

###### 混合函数

- java_method(class,method [,arg1 [,arg2])
- reflect(class,method [,arg1 [,arg2..]])
- hash(a1 [,a2...])

##### 集合操作

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

```



##### 字典操作

###### map类型

取值

```mysql
select b['key1'] from xmp_data_mid.map_test;
select if(b['key1'] is null,'kong',b['key1']) from xmp_data_mid.map_test;
select nvl(b['key1'],'kong') from xmp_data_mid.map_test;
```

转化

```mysql
# 将字符串转化为map类型
select str_to_map('1=2&3=4','&','='); 
# --结果：{"1":"2","3":"4"}
```

问题

>  能不能将一个map中的数据导入到另一个map中？

```mysql
# map类型可以直接插入到另一个map类型中
insert into xmp_data_mid.map_test select 'vvvv',b from xmp_data_mid.map_test;
# 如果map里嵌了一个map，则里面的map的是字符串，不能直接被查询
```

###### json字符串

取值

```mysql
# 从json字符串中取值
get_json_object(string json_string, string path)
# select a.timestamp, get_json_object(a.appevents, ‘$.eventid’), get_json_object(a.appenvets, ‘$.eventname’) from log a;
```

> 注意json字符串不能连续的取值：
>
> ```mysql
> get_json_object(get_json_object(content,'$.ed'),'$.clickid') as clickid,
> ```

转化

```mysql
# json字符串转map对象
select regexp_replace('{"张":"二","李":"小"}','\\}|\\{', '');
select str_to_map(regexp_replace('{"张":"二","李":"小"}','\\}|\\{', ''));
-- 转化的结果是：{"\"李\"":"\"小\"","\"张\"":"\"二\""}

select regexp_replace('{张:二,李:小}','\\}|\\{', '');
select str_to_map(regexp_replace('{张:二,李:小}','\\}|\\{', ''));
-- 转化的结果是：{"李":"小","张":"二"}
```

合并

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

#### UDF

udf和streaming的区别在于udf必须是在hadoop平台上的文件，而streaming要求的则是本地文件

##### 编解码

```
hex/unhex（自带）
数据put的时候，二进制数据乱码问题

uridecode/uriencode
字符串中有空格等的风险，如url参数传递，通常编码后再传

md5
计算md5值（自带）
```

##### 数据类型转换

str->map

> str_to_map(strings ,delim1,delim2), delin1键值对分隔符，delim2键值分隔符

```mysql
select str_to_map('k1:v1,k2:v2',',',':'); # {"k1":"v1","k2":"v2"}
```

str->array

> split(strings,pattern)

```mysql
select split('5.2.4.1234','\\.');  # ["5","2","4","1234"]
```

array->str

> concat_ws(delim,ARRAY arr)

```mysql
select concat_ws('_',fu5) from xmp_odl.xmpplaydur where ds='20170612' and hour=10 limit 10;
select concat_ws('_',["5","2","4","1234"]);
```

以上均是自带的，以下是扩展：

array->map

```python
# 比如k1,v1,k2,v2,其顺序依次是key,value,key,value,可以参考python-streaming实现
a = [1, 2, 3, 4, 5, 6]
b=list(zip( a[::2], a[1::2] )) # [(1, 2), (3, 4), (5, 6)]
dict(b) #{1: 2, 3: 4, 5: 6}
```

##### 分析函数

```mysql
# 待补充
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

##### transform

结合insert overwrite 使用transform

```mysql
add file python_streaming.py;
select transform(substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time) 
using 'python_streaming.py' 
as (pid,mlint,flstr,sstr,fip,ftime)
from xmp_odl.xmpplaydur where ds='$date' limit 1000;
```

> 可以直接将经过处理后的文件进行处理后导出到本地

#####  reduce

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

### 积累

#### url解析

##### url还原

上报的url大多都经过uriencode进行编码，对`[:?,/]`等进行编码，若要正常解析，先使用uridecode对url解析，如下：

```
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

##### url参数解析

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

#### ip处理

通过ip处理，获取位置等信息

ipstr->int

```

```

int->ipstr

> 暂时没有查找到关于ip的函数，需要自定义实现

```

```

#### 文件名处理

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

#### 关键词过滤

> 关键词过滤的核心是如何批量处理关键词的问题

### 优化

#### 多表join

优化代码结构

```
select .. from join tables (a,b,c) with keys (a.key, b.key, c.key) where ....   
```

关联条件相同多表join会优化成一个job

#### left semi join

left semi join是可以高效实现in/exists子查询的语义，

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

#### 设置参数

设置reduce的个数

```hive
set mapred.reduce.tasks=18;
```

#### 数据倾斜

//待完善

### 备份

#### 迁移

数据迁移指的是在不同的hive数据仓库或者不同的hive集群上进行数据的迁移

**结构迁移**

结构迁移可以跨库

```mysql
create table db1.xxx like db2.xxx;
```

**结构和数据迁移**

```mysql
create table db1.xxx as select * from db2.xxx;
```

> 不确定分区是否也一起迁移了，或者迁移的数据是否也按分区

#### 导入

```mysql
load data local inpath '/liguodong/hive/data' into table employee;
```

#### 导出

```mysql
insert overwrite local directory '/home/wyp/wyp' select * from wyp;
```

### 问题

#### 面试

//待补充

#### 查询

##### join时候字段非相等操作

问题描述：

​	Both left and right aliases encountered in JOIN 's1'

解决方法

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

## 参考

- 基础

  [官方参考手册（注意官方函数参考）](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DML#LanguageManualDML-Delete)

  ​[hive array、map、struct使用](http://blog.csdn.net/yfkiss/article/details/7842014)

- 函数

  [HIVE 时间函数](http://www.cnblogs.com/moodlxs/p/3370521.html)

  [HIVE字符串函数](https://www.iteblog.com/archives/1639.html)

  [HIVE数学函数](http://blog.csdn.net/zhoufen12345/article/details/53608271)

  [HIVE常见内置函数及其使用(推荐)](http://blog.csdn.net/scgaliguodong123_/article/details/46954009)(还有要探索的地方)

- 查询

  [连接参考](http://www.cnblogs.com/pcjim/articles/799302.html)

- 积累

  [HIVE数据迁移](http://blog.csdn.net/u9999/article/details/34119441)

  [Hive SQL: Both left and right aliases encountered in JOIN](https://stackoverflow.com/questions/36015035/hiv	e-sql-both-left-and-right-aliases-encountered-in-join)

- 优化

  [Hive join数据倾斜解决方案](http://www.cnblogs.com/ggjucheng/archive/2013/01/03/2842821.html)