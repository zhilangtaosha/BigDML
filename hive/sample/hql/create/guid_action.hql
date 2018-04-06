use xmp_data_mid;
CREATE TABLE `guid_action`(
  `guid` string, 
  `flag1` string, 
  `flag2` string, 
  `flag3` string, 
  `num` int)
PARTITIONED BY ( 
  `dtask` string, 
  `dyear` string, 
  `dmon` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'field.delim'='\t', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.SequenceFileInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat';


-- 开启本地模式
set hive.exec.mode.local.auto=true;

-- 分区表在插入的时候所有分区必须指定
insert into table guid_action partition(dtask='test',dyear='test',dmon='test') select '1','zhangsan','boy','北京',22;
insert into table guid_action partition(dtask='test',dyear='test',dmon='test') select '2','lisi','girl','天津',22;
insert into table guid_action partition(dtask='test',dyear='test',dmon='test') select '3','wangwu','boy','上海',23;
