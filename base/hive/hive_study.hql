-------------- 基础
# 创建表
# 文本格式存储
use kankan_odl;drop table if exists hive_table_templete;
create external table if not exists hive_table_templete(
  subid int,
  peerid string,
  movieid int)
partitioned by (ds string)
row format delimited
fields terminated by '\t'
stored as textfile;

# 序列化格式存储
use kankan_odl;drop table if exists hive_table_templete;
create external table if not exists union_install(
   Fu1 string,
   Fu2 string,
   Fu3 string,
   Fu4 string,
   Fu5 string,
   Fu6 string,
   Fu7 string,
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
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat';


# 建表样例：
CREATE EXTERNAL TABLE xx.xx(
  `guid` string, 
  `phonetype` string, 
  `channelid` string, 
  `ip` string, 
  `sessionid` string, 
  `network` string, 
  `version` string, 
  `userid` string, 
  `movieid` string, 
  `model` string, 
  `sab` string, 
  `rsessionid` string, 
  `rn` string, 
  `refreshid` string, 
  `position` string, 
  `refreshnum` string, 
  `ts` bigint, 
  `ownerid` string, 
  `owner_type` string, 
  `video_type` string, 
  `duration` string, 
  `retype` string, 
  `source` string)
PARTITIONED BY ( 
  `ds` string, 
  `page` string, 
  `card` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'colelction.delim'=',', 
  'field.delim'='\t', 
  'mapkey.delim'=':', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.SequenceFileInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat';





# 导入数据
ihql="use kankan_odl;delete from tbname where ds='${date}';load data local inpath '/home/work/test.txt' into table tbname;"
${HIVE} -e "${chql}"

# 导出数据
esql="use kankan_odl;select '${date}',fu3,fu2,count(*) from xmpcloud2 where ds='${date}' and length(fu4)=16 group by fu3,fu2;"
${HIVE} -e "${esql}" > $datapath/xmp_cloud_${date}



# 导出数据到本地文件(并指定字段分割方式)
insert overwrite local directory '/tmp/xx' row format delimited fields terminated by '\t' select * from test;

# hive写本地数据
insert overwrite local directory '/data/access_log/access_log.45491' row format delimited fields terminated by ' ' collection items terminated by ' ' select *

# hive修改表的存储属性
alter TABLE  pusherdc   SET FILEFORMAT
INPUTFORMAT "org.apache.hadoop.mapred.SequenceFileInputFormat"
OUTPUTFORMAT "org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat";

# hive显示分区
use xmp_odl;show partitions $tbl partition(ds='$date');

# hive添加分区
use xmp_odl;alter table $tbl add if not exists partition (ds='$date',hour='$hour');

# hive删除分区
use xmp_odl;alter table $tbl drop partition(ds='20160808',hour='00');

# hive修改分区
use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') set location "/user/kankan/warehouse/..."
use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') rename to partition(ds='20160808',hour='01')


# hive添加列
use xmp_odl;alter table $tbl add columns(col_name string);

# hive修改列
use xmp_odl;alter table $tbl change col_name newcol_name string [after x] [first];

# hive表重命名
use xmp_odl;alter table $tbl rename to new_tbl_name;


------------------ 其它
-- 演示表创建
use xmp_data_mid;
insert overwrite table filters_load partition(type='accum')
select hour,count(*) from xmp_odl.zkpv where ds='20160702' group by hour order by hour;

-- 累积条数
select hour
    ,count(*) as hour_cnt
    ,sum(count(*)) over (order by hour rows between unbounded preceding and current row) as accum_cnt
from 
    xmp_odl.zkpv 
where ds='20160702' 
group by hour;

-- 累积条数、累积和、累积均值、3步移动平均
select id as hour,f1 as cnt
	,sum(f1) over(order by id rows between unbounded preceding and current row) -- 累积和
    ,sum(f1) over(order by id rows between 1 preceding and 1 following)         -- 前后一小时之和
    ,avg(f1) over(order by id rows between unbounded preceding and current row) -- 累积均值
    ,avg(f1) over(order by id rows between 3 preceding and current row)         -- 前3小时的均值
from
    xmp_data_mid.filters_load
where type='accum'
group by id,f1;


---------------- join
--1.left semi join(两种写法结果相同)
select 
    *
from 
(select * from tbl_a where dtask='tjoin')a
left semi join
(select * from tbl_b where dtask='tjoin')b
on a.id=b.id;

select 
    *
from 
tbl_a a
left semi join
tbl_b b
on a.dtask=b.dtask and a.id=b.id and a.dtask='tjoin';


--2.left join （两种写法结果不同）
select 
    *
from 
(select * from tbl_a where dtask='tjoin')a
left join
(select * from tbl_b where dtask='tjoin')b
on a.id=b.id;


select 
    *
from 
    tbl_a a
left join
    tbl_b b
on a.dtask=b.dtask and a.id=b.id and a.dtask='tjoin';


-- 用笛卡尔积实现遍历
use xmp_data_mid;
select a.funnel_level,b.id 
from 
    funnel_test a
left join
    high_test b
on(true)
where a.funnel_level<=b.id;