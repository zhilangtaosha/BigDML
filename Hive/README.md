## HIVE积累

[TOC]

### 基础

#### 数据类型

string

```mysql
# 字符串分割(返回数组)
split('xxx_we2_23','_')  
```

array

```mysql
# 求array的长度
size(arrya)
# # 如何将计算的数据直接在本行内使用呢
select split("wew_w23_ew0","_") inner ji,select size(split("wew_w23_ew0",'_')) as cnt
```

map

```

```

struct

```mysql

```

#### 命令行

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



### 创建表

#### 文本格式存储
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

#### 序列化格式存储
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

### 查询

#### 基本查询

> 不嵌套，只使用最基本的，无关联

##### case when ..  then  .. else  .. end as .. 

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

例子：

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
from xmpplaydur where size(fu5)!=0 and fu5[0]>=1023
```

##### coalesce

COALESCE( value1,value2,... )

The COALESCE function returns the fist not NULL value from the list of values. If all the values in the list are NULL, then it returns NULL.

```mysql
select COALESCE(NULL,1,"ww") from test.dual;
```

> 如何返回数组中的第一个非NULL元素，配合collect_list使用？



#### 子查询

```mysql
select a.mt,count(*) as cnt from (select from_unixtime(finsert_time,'yyyyMMdd HH:mm:ss') as mt from xmp_odl.xmp_pv where ds='20161206') a group by a.mt order by cnt desc;
```

#### 正则

```mysql
# 正则匹配
select  'abc'  regexp '^[a-z]*$'   from test.dual;
select  'http://v.xunlei.com'  regexp 'http://v.xunlei.com/?$'   from test.dual; //true

# 正则抽取（注意此处不能使用\d和\w等类似的字符）
select regexp_extract('http://xxx/details/0/40.shtml','http://xxx/details/([0-9]{1,})/([0-9]{1,})\.shtml',1) from test.dual; # 返回40


# 正则替换
select regexp_replace('foobar','oo|ba','') from test.dual; # 返回fr
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



```

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

####  连接

例1

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

例2：

```mysql
select case when (fu6>=0 and fu6<1024) then '[0,1)' when (fu6>=1024 and fu6<2048) then '[1,3)' when (fu6>=2048 and fu5<3072) then '[2,3)' when (fu6>=3072 and fu6<4096) then '[3,4)' when fu6>=4096 then '[4,)' else 'error' end as 'dur',if((lower(fu7) regexp "geforce") ,'yes','no'),count(*) from xmp_odl.xmpcloud2 where ds='20170618' and fu3='2341' and fu2 in (3,4,5) group by substr(fu6,1,1),if(( lower(fu7) regexp "geforce"),'yes','no') order by tsize;
```



### 数据导入导出

#### 导入数据

```shell
ihql="use kankan_odl;delete from tbname where ds='${date}';load data local inpath  '/home/work/test.txt' into table tbname;"
${HIVE} -e "{chql}"
```

#### 导出数据

```shell
esql="use kankan_odl;select '{date}',fu3,fu2,count(*) from xmpcloud2 where ds='{date}' and length(fu4)=16 group by fu3,fu2;"
${HIVE} -e "{esql}" > datapath/xmp_cloud_{date}
```

- 导出数据到本地文件(并指定字段分割方式)

```sql
insert overwrite local directory '/tmp/xx' row format delimited fields terminated by '\t' select * from test;
```

- hive写本地数据

```sql
insert overwrite local directory '/data/access_log/access_log.45491' row format delimited fields terminated by ' ' collection items terminated by ' ' select *
```

### 属性修改

#### 分区操作

##### 显示分区

`use xmp_odl;show partitions $tbl partition(ds='$date');`

##### 添加分区
`use xmp_odl;alter table $tbl add if not exists partition (ds='$date',hour='$hour');`

##### 删除分区
`use xmp_odl;alter table $tbl drop if exists partition(ds='20160808',hour='00');`

##### 修改分区
```sql
use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') set location "/user/kankan/warehouse/..."
use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') rename to partition(ds='20160808',hour='01')
```

#### 列操作


##### 添加列
`use xmp_odl;alter table $tbl add columns(col_name string);`

##### 修改列
`use xmp_odl;alter table $tbl change col_name newcol_name string [after x][first];`

##### 删除列

`use xmp_odl;alter table $tbl drop?`

#### 表操作

##### 表重命名

`use xmp_odl;alter table $tbl rename to new_tbl_name;`

##### 修改存储属性

```sql
# 修改存储格式
alter TABLE  pusherdc   SET FILEFORMAT
INPUTFORMAT "org.apache.hadoop.mapred.SequenceFileInputFormat"
OUTPUTFORMAT "org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat";

# 修改字段分割方式
alter table xmp_subproduct_install set SERDEPROPERTIES('field.delim' = '\u0001');
```

##### 删除表

> 对外部表（存储在本地文件系统）和内部表（存储在MetaStore），删除语句相同
>
> ` drop table if exists $tbl`

删除的时候会连分区和文件(内部表)一起删除

### 函数

#### 日期时间操作

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

参考:[HIVE时间操作函数](http://www.cnblogs.com/moodlxs/p/3370521.html)

#### 字符串

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



## 参考

[官方参考手册](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DML#LanguageManualDML-Delete)

[hive array、map、struct使用](http://blog.csdn.net/yfkiss/article/details/7842014)

[HIVE 时间操作函数](http://www.cnblogs.com/moodlxs/p/3370521.html)

[HIVE常用字符串操作函数](https://www.iteblog.com/archives/1639.html)

[HIVE常见数学函数](http://blog.csdn.net/zhoufen12345/article/details/53608271)

[HIVE常见内置函数及其使用(推荐)](http://blog.csdn.net/scgaliguodong123_/article/details/46954009)